import time
import api.web
import api.autorules
from api.mongo import evetomongo
from core.checkstart import start
from lib.data import config, clean_status,src_ip,dest_ip
from api.mongo import clean_mongo, show_db,show_ioc
from api.logger import logger
import os
import json
from flask import Flask, request, redirect, url_for, jsonify, send_from_directory, make_response, Response


app = Flask(__name__)
@app.route('/api/map', methods=['GET'])
def map():
    begintime = request.args.get("begintime")
    endtime = request.args.get("endtime")
    result = api.web.map(begintime=begintime, endtime=endtime)
    return Response(json.dumps(result, ensure_ascii=False),
                    mimetype='application/json')


@app.route('/api/evefile', methods=['GET', 'POST'])
def upload_evefile():
    if request.method == 'POST':
        config['client_ip'] = request.remote_addr
        filename = request.files['clientfile'].filename
        file = request.files['clientfile'].readlines()
        evetomongo(eve_file=file)
        logger.info("{} 提交了日志 {}".format(request.remote_addr, filename))
        return "upload eve.json success"


@app.route('/api/db', methods=['GET', 'POST'])
def clean_db():
    if request.method == 'GET':
        result = show_db()
        return result
    if request.method == 'POST':
        logger.warning("{} 请求清理数据库,等待服务端处理".format(request.remote_addr))
        clean_status['clean_db'] = "waiting process"
        return "start clean db"


@app.route('/api/status', methods=['GET'])
def get_status():
    status = api.web.get_status()
    return status

@app.route('/api/cleanstatus',methods=['GET'])
def get_clean_status():
    return clean_status['clean_db']


@app.route('/api/rules', methods=['GET', 'POST'])
def set_rules():
    if request.method == 'POST':
        set_info = request.get_data().decode('utf-8')
        set_rules_info = json.loads(set_info)
        api.web.set_clientrules(set_rules_info['rules_info'])
        logger.info("防御策略变更")
        return "ok"
    elif request.method == 'GET':
        server = request.args.get('server')
        query = request.args.get('search')
        allrules = {}
        if query != None:
            allrules['rules'] = api.web.get_allrules(server, query)
        else:
            allrules['rules'] = api.web.get_allrules(server)
        return jsonify(allrules)


@app.route('/api/rules/del', methods=['POST', 'DELETE'])
def del_client_rules():
    if request.method == 'POST':
        del_info = request.get_data().decode('utf-8')
        del_id = json.loads(del_info)['id']
        del_result = api.web.del_rules(del_id)
        logger.warning("{} 规则删除".format(del_id))
        return del_result
    if request.method == 'DELETE':
        del_result = api.web.del_rules("all")
        logger.warning("防御策略重置")
        return del_result


@app.route('/api/rules/change', methods=['POST'])
def change_client_rules():
    if request.method == 'POST':
        change_info = request.get_data().decode('utf-8')
        change_id = json.loads(change_info)['id']
        change_type = json.loads(change_info)['type']
        api.web.change_rules(change_id, change_type)
        logger.info("{} 更改防御方式为 {}".format(change_id, change_type))
        return "{} changed to type {}".format(change_id, change_type)


@app.route('/api/vulsearch', methods=['POST'])
def vul_search():
        query = json.loads(request.get_data().decode('utf-8'))
        search_result = api.web.vul_search(query['query'])
        result = {}
        result['data'] = search_result
        try:
            result['count'] = src_ip[query['query']]   
        except :
            try:
                result['count'] = dest_ip[query['query']]
            except :
                pass
        return jsonify(result)


@app.route('/api/downloadlog', methods=['GET'])
def down_log():
    return send_from_directory('./', 'log.txt', as_attachment=True)


@app.route('/install.sh')
def send_install_file():
    logger.info("{} 开始安装".format(request.remote_addr))
    install_file = api.web.customization_install(request.remote_addr)
    return install_file


@app.route('/local.rules')
def get_clientrules():
    logger.info("{} 更新了防御策略".format(request.remote_addr))
    clientrules = open(
        './ThirPath/suricata/marioips/rules/local.rules', 'r')
    rulesfile = clientrules.read()
    clientrules.close()
    return rulesfile


@app.route('/marioips.tar.gz')
def send_conf_tar():
    logger.info("{} 下载客户端主程序".format(request.remote_addr))
    file_dir = os.getcwd() + "/ThirPath/suricata/"
    api.web.make_tar()
    response = make_response(send_from_directory(
        file_dir, "marioips.tar.gz", as_attachment=True))
    return response


@app.route('/api/setting', methods=['GET', 'POST'])
def setting():
    if request.method == 'GET':
        return api.web.show_setting()
    if request.method == 'POST':
        new_settings = json.loads(request.get_data().decode('utf-8'))
        change_result = api.web.change_setting(new_settings)
        return change_result


@app.route('/api/update', methods=['GET'])
def checkupdate():
    operation = request.args.get('operation')
    if operation == "check":
        try:
            config['update_setting_time']
        except :
            config['update_setting_time'] = 'no update'
        return str(config['update_setting_time'])

@app.route('/api/wavy',methods=['GET'])
def wavy():
    begintime = request.args.get("begintime")
    endtime = request.args.get("endtime")
    wavy_lists = api.web.show_wavy(begintime,endtime)
    print(wavy_lists)
    return jsonify(wavy_lists)

@app.route('/api/ioc',methods=['GET'])
def ioc_statistical():
    search = request.args.get("search")
    if search == "all":
        statistical = show_ioc()
        return statistical
@app.route('/api/srcip',methods=['GET'])
def count_srcsip():
    result = sorted(src_ip.items(), key=lambda d: d[1],reverse=True)
    src_ip_sorted = {}
    for iterm in result:
        src_ip_sorted[iterm[0]] = int(iterm[1])
    return jsonify(src_ip_sorted)
@app.route('/api/destip',methods=['GET'])
def count_destip():
    result = sorted(dest_ip.items(), key=lambda d: d[1],reverse=True)
    dest_ip_sorted = {}
    for iterm in result:
        dest_ip_sorted[iterm[0]] = int(iterm[1])
    return jsonify(dest_ip_sorted)
if __name__ == '__main__':
    app.config['JSON_AS_ASCII'] = False
    app.config['JSON_SORT_KEYS'] = False
    app.run(host='0.0.0.0',debug=True)
