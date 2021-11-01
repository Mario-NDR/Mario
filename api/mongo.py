import pymongo,sys
import re
from api.es import insert_es,search_es,get_all_index
from pymongo.message import update
from api.logger import logger
import urllib
import json
import api.analyze
import time
import configparser
def connect(mongo_url):
    count = 0
    while True:
        client = pymongo.MongoClient(mongo_url, serverSelectionTimeoutMS=3)
        try:
            client.admin.command("ping")
        except:
            count += 1
        else:
            break
        if count == 3:
            return False
    return client
def get_mongo():
    config = configparser.ConfigParser()
    config.read('config.cfg')
    return "mongodb://{}:{}@{}:{}/".format(config['mongodb']['username'],config['mongodb']['password'],config['mongodb']['host'],config['mongodb']['port'])
def mongo_connect():
    monto_url = get_mongo()
    if connect(monto_url) != False:
        logger.info("数据库连接成功")
    else:
        logger.error("请检查数据库设置")
        sys.exit()

def evetomongo(client_ip,eve_file=None):
    insert_data = {}
    now_status = getstatus_db()
    try:
        timediff = int(time.time()) - now_status['last_clean']
        if timediff > 3600:
            now_status['clean_db'] = "waiting process"
            print("auto")
    except:
        now_status['last_clean'] = int(time.time())
    if now_status['clean_db'] == "waiting process":
        logger.info("数据库清理程序触发")
        now_status['last_clean'] = int(time.time())
        now_status['clean_db'] = "running"
        del_stats()
        clean_mongo()
        now_status['clean_db'] = "ready"
    num = 0
    if eve_file:
        eve_lines = eve_file
        for eve_line in eve_lines:
            try:
                eve_line = json.loads(eve_line.decode('utf-8'))
            except:
                eve_line = json.loads(eve_line)
            if eve_line["event_type"] == "alert" and "app_proto" in eve_line.keys()and any(_ in eve_line["payload_printable"] for _ in ["wget","curl"]):
                downloadfile_url = re.findall(r'(wget|curl).+(http[s]{0,1}://\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}(\:\d{1,5}){0,1}[a-zA-z0-9\/\.\/\_]+)',urllib.parse.unquote(eve_line["payload_printable"]))
                logger.info("检测到样本传播 {}".format(downloadfile_url[0][1]))
            eve_line['client_ip'] = client_ip
            if eve_line["event_type"] not in insert_data.keys():
                insert_data[eve_line["event_type"]] = []
            insert_data[eve_line["event_type"]].append(eve_line)
            # insert_es(eve_line["event_type"],eve_line)
            num += 1
        now_status['total'] += num
        insert_es(insert_data)
        logger.info("新增数据{}条".format(num))
        api.analyze.analyze_suricata_alert()
    update_config(now_status)
    return num

def getstatus_db():
    mongo_url = get_mongo()
    myclient = pymongo.MongoClient(mongo_url, connect=False)
    mydb = myclient["mariodb"]
    mycol = mydb['mario_config']
    col_result = mycol.find_one({})
    return col_result

def update_config(newconfig,mod="update"):
    mongo_url = get_mongo()
    myclient = pymongo.MongoClient(mongo_url, connect=False)
    mydb = myclient["mariodb"]
    mycol = mydb['mario_config']
    if mod == "new":
        mycol.insert_one(newconfig)
    else:
        mycol.update_one({},{"$set":newconfig})
    

def findeve(index_name, begintime=None, endtime=None):
    if begintime and endtime:
        infos = search_es(index_name,begintime,endtime)
        return infos
    else:
        infos = search_es(index_name,limit=10000)
        return infos


def show_db():
    now_status = getstatus_db()
    db_info = {}
    db_info['data'] = []
    db_info['sum'] = 0
    db_info['total'] = now_status['total']
    try:
        db_info['last_clean'] = now_status['last_clean']
    except:
        now_status['clean_db'] = "waiting process"
        db_info['last_clean'] = "Never run cleaning procedures"
    for coll in get_all_index():
        db_info['sum'] += coll['count']
        db_info['data'].append(coll)
    return json.dumps(db_info)


def del_stats():
    myclient = pymongo.MongoClient(get_mongo(), connect=False)
    mydb = myclient["mariodb"]
    # for colname in ["stats","flow"]:
    #     mycol = mydb[colname]
    #     mycol.delete_many({})
    logger.info("流量日志状态更新")
    myclient.close()


def clean_mongo():
    now_status = getstatus_db()
    now_status['last_clean'] = int(time.time())
    src_iplist = []
    myclient = pymongo.MongoClient(get_mongo(), connect=False)
    mydb = myclient["mariodb"]
    alert_info = mydb['alert']
    coll_names = mydb.list_collection_names(session=None)
    for alert in alert_info.find():
        src_iplist.append(str(alert['src_ip']))
    for coll in coll_names:
        db = mydb[coll]
        del_id = []
        del_count = 0
        if coll == "fileinfo":
            del_count += db.find({"fileinfo.filename": {"$regex": "eve_.*json"}}).count()
            db.delete_many({"fileinfo.filename": {"$regex": "eve_.*json"}})
            del_count += db.find({"fileinfo.filename": {"$regex": "/api/"}}).count()
            db.delete_many({"fileinfo.filename": {"$regex": "/api/"}})
            del_count += db.find({"fileinfo.filename": {"$regex": "local.rules"}}).count()
            db.delete_many({"fileinfo.filename": {"$regex": "local.rules"}})
        if coll in ['alert','flow','stats','mario_config']:
            continue
        logger.info("清理数据库 {}".format(coll))
        for item in list(db.find().batch_size(500)[:]):
            try:
                if item['src_ip'] not in src_iplist:
                    del_id.append(item['_id'])
                else:
                    continue
            except:
                del_id.append(item['_id'])
                continue
        for data_id in del_id:
            query = {"_id": data_id}
            delresult = db.delete_one(query)
            del_count += delresult.deleted_count
        logger.warning("清理 {} 条数据".format(del_count))
    myclient.close()


def show_ioc():
    mongo_url = get_mongo()
    myclient = pymongo.MongoClient(mongo_url, connect=False)
    try:
        mydb = myclient["azkaban"]
    except:
        logger.warning("无 IOC 插件")
        return "no ioc plug"
    coll_names = mydb.list_collection_names(session=None)
    db_info = {}
    db_info['data'] = []
    db_info['sum'] = 0
    for coll in coll_names:
        db = mydb[coll]
        info = {}
        info['name'] = coll
        info['count'] = db.find().count()
        db_info['sum'] += info['count']
        db_info['data'].append(info)
    return json.dumps(db_info)
