from api.logger import logger
from api.mongo import getstatus_db,mongo_connect,update_config
import datetime






def start():
    mongo_connect()
    now_status = getstatus_db()
    if now_status == None:
        now_status = {}
        now_status['clean_db'] = "ready"
        update_config(now_status,"new")
    if 'starttime' not in now_status.keys():
        now_status['starttime'] = datetime.datetime.now()
    if 'total' not in now_status.keys():
        # running_status['total'] = 0
        now_status['total'] = 0
    update_config(now_status)