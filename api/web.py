import os
import re
import tarfile
import json
import psutil
from pymongo.message import update
from api.logger import logger
import time
import datetime
import requests
import api.analyze
from api.ip import ipAnalysis
import socket
from api.mongo import update_config,getstatus_db
from lib.data import  classtype
from flask import redirect, url_for


def map(begintime=None, endtime=None):
    result = api.analyze.analyze_suricata_alert(
        data="xy", language="zh-CN", begintime=begintime, endtime=endtime)
    return result


def ip(begintime=None, endtime=None):
    ipResult = api.analyze.analyze_suricata_alert(
        data="ip", begintime=begintime, endtime=endtime)
    return ipResult


def make_tar():
    try:
        os.remove("{}/ThirPath/marioips/marioips.tar.gz".format(os.getcwd))
    except:
        pass
    with tarfile.open("./ThirPath/marioips/marioips.tar.gz", "w:gz") as tar:
        tar.add("./ThirPath/marioips/",
                arcname=os.path.basename("./ThirPath/marioips/"))


def get_allrules(server, query=" "):
    allrules = []
    if server == "client":
        originalrules_file = open(
            './ThirPath/marioips/rules/local.rules', 'r')
    else:
        originalrules_file = open(
            './ThirPath/marioips/rules/all.rules', 'r')
    originalrules = originalrules_file.readlines()
    for originalrule in originalrules:
        rule_info = {}
        rule_info['msg'] = re.findall(
            r'"(.*?)"', originalrule, re.S)[0]
        rule_info['sid'] = re.findall(
            r'sid:(.*?);', originalrule, re.S)[0].strip()
        if query == rule_info['sid'] or query.lower() in rule_info['msg'].lower():
            if server == "client":
                rule_info['type'] = re.findall(
                    r'^(.*?) ', originalrule, re.S)[0]
            rule_info['content_type'] = re.findall(
                r' (.*?) ', originalrule, re.S)[0].upper()
            try:
                rule_info['class_type'] = classtype[re.findall(
                    r'classtype:(.*?);', originalrule, re.S)[0]]
            except:
                try:
                    rule_info['class_type'] = re.findall(
                        r'classtype:(.*?);', originalrule, re.S)[0]
                except:
                    rule_info['class_type'] = "未定义"
            allrules.append(rule_info)
    originalrules_file.close()
    return allrules


def set_clientrules(rules_info):
    now_status = getstatus_db()
    now_status['update_setting_time'] = int(time.time())
    with open('./ThirPath/marioips/rules/local.rules', 'r') as now_rules:
        rules = now_rules.readlines()
        rules_id = []
        for rule in rules:
            sid = re.findall(r'sid:(.*?);', rule, re.S)[0].strip()
            rules_id.append(sid)
    originalrules_file = open(
        './ThirPath/marioips/rules/all.rules', 'r')
    originalrules = originalrules_file.readlines()
    clientrules_file = open(
        './ThirPath/marioips/rules/local.rules', 'a+')
    for info in rules_info:
        for rule in originalrules:
            sid = re.findall(
                r'sid:(.*?);', rule, re.S)[0].strip()
            if info['id'] == sid not in rules_id:
                clientrules_file.write(rule.replace(
                    re.search(r'^(.*?) ', rule, re.S).group(0), info['type'] + " "))
    clientrules_file.close()
    originalrules_file.close()
    update_config(now_status)
    return "yes"


def del_rules(del_sid):
    now_status = getstatus_db()
    now_status['update_setting_time'] = int(time.time())
    reman_rules = []
    if del_sid == "all":
        with open('./ThirPath/marioips/rules/local.rules', 'w') as f:
            f.truncate()
        return "del all rules ok"
    del_result = "del false"
    with open('./ThirPath/marioips/rules/local.rules', 'r') as clientrules_file:
        for rules in clientrules_file:
            sid = re.findall(
                r'sid:(.*?);', rules, re.S)[0].strip()
            if sid != del_sid:
                reman_rules.append(rules)
            else:
                del_result = "del rules {} ok".format(del_sid)
    with open('./ThirPath/marioips/rules/local.rules', 'w') as f:
        for rules in reman_rules:
            f.write(rules)
    update_config(now_status)
    return del_result


def change_rules(change_sid, chang_type):
    now_status = getstatus_db()
    now_status['update_setting_time'] = int(time.time())
    reman_rules = []
    del_result = "del false"
    with open('./ThirPath/marioips/rules/local.rules', 'r') as clientrules_file:
        for rules in clientrules_file:
            sid = re.findall(
                r'sid:(.*?);', rules, re.S)[0].strip()
            if sid != change_sid:
                reman_rules.append(rules)
            else:
                rules_type = re.findall(
                    r'^(.*?) ', rules, re.S)[0]
                rules = rules.replace(rules_type, chang_type)
                reman_rules.append(rules)
    with open('./ThirPath/marioips/rules/local.rules', 'w') as f:
        for rules in reman_rules:
            f.write(rules)
    update_config(now_status)
    return del_result


def customization_install(src_ip):
    netcard_info = []
    info = psutil.net_if_addrs()
    for k, v in info.items():
        for item in v:
            if item[0] == 2 and not item[1] == '127.0.0.1':
                netcard_info.append(item[1])
    src_ip = re.findall(r'[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}', src_ip, re.S)[0]
    for ip in netcard_info:
        if src_ip in ip:
            install_ip = ip
        else:
            continue
    try:
        install_file = open(os.getcwd() + "/ThirPath/marioips/install.sh", "r")
        file_read = install_file.read().replace("ipadd", install_ip)
        install_file.close()
        return file_read
    except:
        install_file = open(os.getcwd() + "/ThirPath/marioips/install.sh", "r")
        file_read = install_file.read().replace("ipadd", ipAnalysis.get_local_ip()[0])
        install_file.close()
        return file_read


def search_venuseye(query):
    result = {}
    result['vendor'] = '启明星辰金睛'
    if re.findall(r'\d+\.\d+\.\d+\.\d+', query):
        try:
            search_result = json.loads(requests.post(
                "https://www.venuseye.com.cn/ve/ip", {'target': '{}'.format(query)}).text)
        except Exception as e:
            search_result = 0
    else:
        try:
            search_result = json.loads(requests.post(
                "https://www.venuseye.com.cn/ve/domain", {'target': '{}'.format(query)}).text)
        except:
            search_result = 0
    if search_result != None:
        try:
            result['threat_score'] = search_result['data']['threat_score']
        except:
            result['threat_score'] = 0
        try:
            result['active_time'] = search_result['data']['active_time']
        except:
            result['active_time'] = 'None'
        try:
            result['city'] = search_result['data']['area']
        except:
            result['city'] = 'None'
        try:
            result['operator'] = search_result['data']['operator']
        except:
            result['operator'] = 'None'
        try:
            result['tags'] = search_result['data']['tags']
        except:
            result['tags'] = []
    logger.info("venuseye 查询 {} 成功".format(query))
    return result


def search_virustotal(query):
    result = {}
    result['vendor'] = '全球威胁情报检索引擎'
    headers = {
        "x-apikey": "e6184c04de532cd5a094f3fd6b3ce36cd187e41e671b5336fd69862257d07a9a",
    }
    if re.findall(r'\d+\.\d+\.\d+\.\d+', query):
        url = 'https://www.virustotal.com/api/v3/ip_addresses/{}'.format(query)
    else:
        url = 'https://www.virustotal.com/api/v3/domains/{}'.format(query)
    try:
        search_result = json.loads(requests.get(url, headers=headers).text)
    except:
        search_result = None
    if search_result != None:
        result['engine_result'] = []
        for search_iterm in search_result['data']['attributes']['last_analysis_results']:
            search_iterm_infos = search_result['data']['attributes']['last_analysis_results'][search_iterm]
            if search_iterm_infos['result'] != 'clean' and search_iterm_infos['result'] != 'unrated':
                result['engine_result'].append(
                    search_iterm_infos['engine_name'])
        analysis_results = search_result['data']['attributes']['last_analysis_stats']
        threat_score = analysis_results['malicious'] + \
            analysis_results['suspicious']
        try:
            result['active_time'] = search_result['data']['attributes']['last_modification_date']
        except:
            result['active_time'] = "None"
        try:
            result['threat_score'] = threat_score
        except:
            result['threat_score'] = "None"
    logger.info("virustotal 查询 {} 成功".format(query))
    return result


def vul_search(ip):
    search_result = []
    try:
        search_result.append(search_virustotal(ip))
    except:
        search_result.append({'vendor': '全球威胁情报检索引擎', 'engine_result': ['查询出错'], 'active_time': 'None', 'threat_score': 'None'})
    try:
        search_result.append(search_venuseye(ip))
    except:
        search_result.append({'vendor': '启明星辰金睛', 'threat_score': 'None', 'active_time': 'None', 'city': '', 'operator': '', 'tags': ['查询出错']})

    return search_result


def get_status():
    now_status = getstatus_db()
    start_time = now_status['starttime']
    now_time = datetime.datetime.now()
    time_diff = now_time-start_time
    timestatus = {}
    diss_seconds = time_diff.seconds
    timestatus['minutes'], timestatus['secouds'] = divmod(diss_seconds, 60)
    timestatus['hours'], timestatus['minutes'] = divmod(
        timestatus['minutes'], 60)
    timestatus['days'] = time_diff.days
    return json.dumps(timestatus)


def show_setting():
    setting = {}
    with open('./ThirPath/marioips/bin/senteve.sh', 'r') as script_senteve:
        script_content = script_senteve.read()
        setting['max_logfile_num'] = re.findall(
            r'-ge (.*?) ]', script_content, re.S)[0]
        setting['heartbeat_time'] = re.findall(
            r'sleep (.*?);', script_content, re.S)[0]
    with open('./ThirPath/marioips/marioips.yaml', 'r') as marioips_yaml:
        marioip_setting = marioips_yaml.read()
        setting['save_pcap'] = re.findall(
            r'pcap-log:.+?enabled: (.*?) #setting save_pcap', marioip_setting, re.DOTALL)[0]
        setting['pcap_size'] = re.findall(
            r'\slimit: (.*?b)', marioip_setting)[0]
        setting['save_file'] = re.findall(
            r'file-store:.+?enabled: (.*?) #setting save_file', marioip_setting, re.DOTALL)[0]
    return json.dumps(setting)


def change_setting(settings):
    now_status = getstatus_db()
    with open('./ThirPath/marioips/bin/senteve.sh', 'r') as script_senteve:
        old_base_settings = script_senteve.read()
        max_logfile_num = re.findall(
            r'-ge (.*?) ]', old_base_settings, re.S)[0]
        heartbeat_time = re.findall(
            r'sleep (.*?);', old_base_settings, re.S)[0]
        new_base_settings = old_base_settings.replace(
            max_logfile_num, settings['max_logfile_num']).replace(heartbeat_time, settings['heartbeat_time'])
    with open('./ThirPath/marioips/bin/senteve.sh', 'w') as script_senteve:
        script_senteve.write(new_base_settings)
    # with open('./ThirPath/marioips/marioips.yaml','r') as marioips_yaml:
    #     old_mario_setting = marioips_yaml.read()
    #     save_pcap = re.findall(r'pcap-log:.+?enabled: (.*?) #setting save_pcap',old_mario_setting,re.DOTALL)[0]
    #     pcap_size = re.findall(r'\slimit: (.*?b)',old_mario_setting)[0]
    #     save_file = re.findall(r'file-store:.+?enabled: (.*?) #setting save_file',old_mario_setting,re.DOTALL)[0]
    #     new_mario_settings = old_mario_setting.replace(save_pcap,settings['save_pcap']).replace(pcap_size,settings['pcap_size']).replace(save_file,settings['save_file'])
    # with open('./ThirPath/marioips/marioips.yaml','w') as marioips_yaml:
    #     marioips_yaml.write(new_mario_settings)
    logger.warning("配置文件修改 {}".format(settings))
    now_status['update_setting_time'] = int(time.time())
    update_config(now_status)
    return "修改成功"


def show_wavy(begintime, endtime):
    eve_lines, days = api.analyze.analyze_to_wavy(begintime, endtime)
    wavy_result = {}
    wavy_result['wavy_date'] = {}
    wavy_result['wavy_date']['恶意代码'] = [0]*len(days)
    wavy_result['wavy_date']['木马活动'] = [0]*len(days)
    wavy_result['wavy_date']['网络扫描'] = [0]*len(days)
    wavy_result['wavy_date']['威胁情报'] = [0]*len(days)
    wavy_result['wavy_date']['DOS攻击'] = [0]*len(days)
    wavy_result['wavy_date']['权限尝试'] = [0]*len(days)
    wavy_result['wavy_date']['WEB攻击'] = [0]*len(days)
    wavy_result['wavy_date']['可疑文件名'] = [0]*len(days)
    wavy_result['wavy_date']['其他类型'] = [0]*len(days)
    wavy_result['time'] = days
    for eve_line in eve_lines:
        eve_line = eve_line['_source']
        print(eve_line["alert"]["category"])
        date = datetime.datetime.strptime(
            eve_line["timestamp"], "%Y-%m-%dT%H:%M:%S.%f%z").astimezone(datetime.timezone(datetime.timedelta(hours=8)))
        format_date = datetime.datetime.strftime(date, "%Y-%m-%d")
        date_list_index = days.index(format_date)
        if eve_line["alert"]["category"] == "Executable code was detected":
            wavy_result['wavy_date']['恶意代码'][date_list_index] += 1
            continue
        if eve_line["alert"]["category"] == "Attempted Denial of Service":
            wavy_result['wavy_date']['DOS攻击'][date_list_index] += 1
            continue
        if eve_line["alert"]["category"] == "Web Application Attack":
            wavy_result['wavy_date']['WEB攻击'][date_list_index] += 1
            continue
        if eve_line["alert"]["category"] == "A suspicious filename was detected":
            wavy_result['wavy_date']['可疑文件名'][date_list_index] += 1
            continue
        if eve_line["alert"]["category"] == "A Network Trojan was detected":
            wavy_result['wavy_date']['木马活动'][date_list_index] += 1
            continue
        if eve_line["alert"]["category"] == "Detection of a Network Scan":
            wavy_result['wavy_date']['网络扫描'][date_list_index] += 1
            continue
        if eve_line["alert"]["category"] == "A system call was detected":
            wavy_result['wavy_date']['威胁情报'][date_list_index] += 1
            continue
        if eve_line["alert"]["category"] == "Attempted User Privilege Gain" or eve_line["alert"]["category"] == "Attempted Administrator Privilege Gain":
            wavy_result['wavy_date']['权限尝试'][date_list_index] += 1
            continue
        wavy_result['wavy_date']['其他类型'][date_list_index] += 1
    for date in list(wavy_result['wavy_date'].keys()):
        if all(_ == 0 for _ in wavy_result['wavy_date'][date]):
            del wavy_result['wavy_date'][date]
    return wavy_result
    # for eve_line in eve_lines:
    #     date = datetime.datetime.strptime(eve_line["timestamp"],"%Y-%m-%dT%H:%M:%S.%f%z").astimezone(datetime.timezone(datetime.timedelta(hours=8)))
    #     format_date = datetime.datetime.strftime(date,"%Y-%m-%d")
    #     date_list_index = days.index(format_date)
    #     if eve_line["alert"]["category"] == "Executable code was detected":
    #         wavy_result['wavy_date']['恶意代码'][date_list_index] += 1
    #     else:
    #         wavy_result['wavy_date']['恶意代码'][date_list_index] += 0
    #     if eve_line["alert"]["category"] == "A Network Trojan was detected":
    #         wavy_result['wavy_date']['木马活动'][date_list_index] += 1
    #     else:
    #         wavy_result['wavy_date']['木马活动'][date_list_index] += 0
    #     if eve_line["alert"]["category"] == "Detection of a Network Scan":
    #         wavy_result['wavy_date']['网络扫描'][date_list_index] += 1
    #     else:
    #         wavy_result['wavy_date']['网络扫描'][date_list_index] += 0
    #     if eve_line["alert"]["category"] == "A system call was detected":
    #         wavy_result['wavy_date']['威胁情报'][date_list_index] += 1
    #     else:
    #         wavy_result['wavy_date']['威胁情报'][date_list_index] += 0
    #     if eve_line["alert"]["category"] == "Attempted User Privilege Gain":
    #         wavy_result['wavy_date']['权限尝试'][date_list_index] += 1
    #     else:
    #         wavy_result['wavy_date']['权限尝试'][date_list_index] += 0
    #     if eve_line["alert"]["category"] != "Detection of a Network Scan" and eve_line["alert"]["category"] != "A Network Trojan was detected" and eve_line["alert"]["category"] != "Executable code was detected" and eve_line["alert"]["category"] != "A system call was detected":
    #         wavy_result['wavy_date']['其他类型'][date_list_index] += 1
    #     else:
    #         wavy_result['wavy_date']['其他类型'][date_list_index] += 0
    # return wavy_result
