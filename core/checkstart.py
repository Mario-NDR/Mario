from lib.data import running_status,config,clean_status
from api.logger import logger
import sys
from api.ip import ipAnalysis
import datetime
import pymongo

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

def mongo_connect():
    if connect("mongodb://root:example@0.0.0.0:27017/") != False:
        config['mongo_url'] = "mongodb://root:example@0.0.0.0:27017/"
        logger.info("数据库连接成功")
    else:
        if connect("mongodb://root:example@34.64.197.155:27017/") != False:
            config['mongo_url'] = "mongodb://root:example@34.64.197.155:27017/"
            logger.info("数据库连接成功")
        else:
            logger.error("请检查数据库设置")
            sys.exit()

def check_env():
    config['ip'] = ipAnalysis.get_local_ip()
    mongo_connect()

def start():
    check_env()
    try:
        clean_status['clean_db']
    except :
        clean_status['clean_db'] = "ready"
    try:
        running_status['starttime']
    except:
        running_status['starttime'] = datetime.datetime.now()
    try:
        running_status['total']
    except :
        running_status['total'] = 0