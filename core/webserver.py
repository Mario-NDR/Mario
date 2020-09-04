import time
import api.web
from api.mongo import evetomongo
from lib.data import config, clean_status
from api.mongo import clean_mongo, show_db
from api.logger import logger
import os
import json
from flask import Flask, request, redirect, url_for, jsonify, send_from_directory, make_response, Response


def webserver():
    app = Flask(__name__)
    @app.route('/api/map', methods=['GET'])
    def map():
        begintime = request.args.get("begintime")
        endtime = request.args.get("endtime")
        result = api.web.map(begintime=begintime, endtime=endtime)
        return jsonify(result)

    @app.route('/api/upload', methods=['GET', 'POST'])
    def upload_file():
        if request.method == 'POST':
            file = request.files['file']
            result = api.web.upload_pcap(file)
            return result
        elif request.method == "GET":
            return '''
            <!doctype html>
            <title>Upload new File</title>
            <h1>Upload new File</h1>
            <form action="" method=post enctype=multipart/form-data>
            <p><input type=file name=file>
                <input type=submit value=Upload>
            </form>
            '''

    @app.route('/api/evefile', methods=['GET', 'POST'])
    def upload_evefile():
        if request.method == 'POST':
            config['client_ip'] = request.remote_addr
            file = request.files['clientfile'].readlines()
            evetomongo(eve_file=file)
            return "upload eve.json success"
        elif request.method == "GET":
            return '''
            <!doctype html>
            <title>Upload new File</title>
            <h1>Upload new File</h1>
            <form action="" method=post enctype=multipart/form-data>
            <p><input type=file name=evefile>
                <input type=submit value=Upload>
            </form>
            '''

    @app.route('/api/db', methods=['GET', 'POST'])
    def clean_db():
        if request.method == 'GET':
            result = show_db()
            return result
        if request.method == 'POST':
            logger.warning("{} 请求清理数据库".format(request.remote_addr))
            clean_status['clean_db'] = "waiting process"
            return "start clean db"

    @app.route('/api/rules', methods=['GET', 'POST'])
    def set_rules():
        if request.method == 'POST':
            set_info = request.get_data().decode('utf-8')
            set_rules_info = json.loads(set_info)
            api.web.set_clientrules(set_rules_info['rules_info'])
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
            return del_result
        if request.method == 'DELETE':
            del_result = api.web.del_rules("all")
            return del_result

    @app.route('/api/rules/change', methods=['POST'])
    def change_client_rules():
        if request.method == 'POST':
            change_info = request.get_data().decode('utf-8')
            change_id = json.loads(change_info)['id']
            change_type = json.loads(change_info)['type']
            api.web.change_rules(change_id, change_type)
            return "{} changed to type {}".format(change_id, change_type)

    @app.route('/api/pcap', methods=['POST'])
    def analyze_pcap():
        filename = request.form.get('filename')
        result = api.web.analyze_pcap(filename)
        return result

    @app.route('/api/demo', methods=['POST'])
    def demo_information():
        num = request.form.get('demonum')
        generate_demo_information(int(num))
        result = {}
        result['newdatenum'] = num
        return jsonify(result)

    @app.route('/api/vulsearch', methods=['POST'])
    def vul_search():
        ip = request.form.get('query').strip('\n').strip('\r').strip()
        search_result = api.web.vul_search(ip)
        result = {}
        result['data'] = search_result
        return jsonify(result)

    @app.route('/install.sh')
    def send_install_file():
        logger.info("{} 开始安装".format(request.remote_addr))
        install_file = api.web.customization_install(request.remote_addr)
        return install_file

    @app.route('/local.rules')
    def get_clientrules():
        logger.info("下发防御策略至 {}".format(request.remote_addr))
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
    app.config['JSON_AS_ASCII'] = False
    app.run(host='0.0.0.0', port=5000, debug=True)
