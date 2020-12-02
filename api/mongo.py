import pymongo
from api.logger import logger
import json
from lib.data import config, running_status,src_ip
from core.checkstart import start
import api.analyze
import time
from datetime import datetime
from lib.data import config, clean_status


def evetomongo(eve_file=None):
    try:
        config['mongo_url']
    except:
        start()
    try:
        timediff = int(time.time()) - db_info['last_clean']
        if timediff > 3600:
            clean_status['clean_db'] = "waiting process"
    except:
        db_info['last_clean'] = "Never run cleaning procedures"
    if clean_status['clean_db'] == "waiting process":
        logger.info("数据库清理程序触发")
        clean_status['clean_db'] = "running"
        del_stats()
        clean_mongo()
        clean_status['clean_db'] = "ready"
    myclient = pymongo.MongoClient(config['mongo_url'], connect=False)
    mydb = myclient["mariodb"]
    num = 0
    if eve_file:
        eve_lines = eve_file
    for eve_line in eve_lines:
        try:
            eve_line = json.loads(eve_line.decode('utf-8'))
        except:
            eve_line = json.loads(eve_line)
        mycol = mydb[eve_line["event_type"]]
        mydict = eve_line
        try:
            mydict['client_ip'] = config['client_ip']
        except Exception as e:
            pass
        mycol.insert_one(mydict)
        num += 1
    running_status['total'] += num
    logger.info("新增数据{}条".format(num))
    myclient.close()
    api.analyze.analyze_suricata_alert()
    return num


def findeve(colname, begintime=None, endtime=None):
    try:
        config['mongo_url']
    except:
        start()
    myclient = pymongo.MongoClient(config['mongo_url'], connect=False)
    mydb = myclient["mariodb"]
    mycol = mydb[colname]
    if begintime and endtime:
        infos = mycol.find({"timestamp": {"$gte": begintime, "$lt": endtime}})
        myclient.close()
        return infos
    else:
        infos = mycol.find()
        myclient.close()
        return infos


def show_db():
    try:
        config['mongo_url']
    except:
        start()
    myclient = pymongo.MongoClient(config['mongo_url'], connect=False)
    mydb = myclient["mariodb"]
    coll_names = mydb.list_collection_names(session=None)
    db_info = {}
    db_info['data'] = []
    db_info['sum'] = 0
    db_info['total'] = running_status['total']
    try:
        db_info['last_clean'] = clean_status['last_clean']
    except:
        clean_status['clean_db'] = "waiting process"
        db_info['last_clean'] = "Never run cleaning procedures"
    for coll in coll_names:
        if coll in ['alert', 'stats']:
            continue
        db = mydb[coll]
        info = {}
        info['name'] = coll
        info['count'] = db.find().count()
        db_info['sum'] += info['count']
        db_info['data'].append(info)
    return json.dumps(db_info)


def del_stats():
    myclient = pymongo.MongoClient(config['mongo_url'], connect=False)
    mydb = myclient["mariodb"]
    for colname in ["stats","flow"]:
        mycol = mydb[colname]
        mycol.delete_many({})
    logger.info("流量日志状态更新")
    myclient.close()


def clean_mongo():
    clean_status['last_clean'] = int(time.time())
    src_iplist = []
    myclient = pymongo.MongoClient(config['mongo_url'], connect=False)
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
        if coll in ['alert','flow','stats']:
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
    try:
        config['mongo_url']
    except:
        start()
    myclient = pymongo.MongoClient(config['mongo_url'], connect=False)
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
