import time
import api.web
import os
from flask import Flask, request, redirect, url_for


def webserver():
    app = Flask(__name__)
    @app.route('/map')
    def map():
        result = api.web.map()
        return result

    @app.route('/ip')
    def ip():
        result = api.web.ip()
        return result

    @app.route('/upload', methods=['GET', 'POST'])
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

    @app.route('/pcap', methods=['POST'])
    def analyze_pcap():
        filename = request.form.get('filename')
        result = api.web.analyze_pcap(filename)
        return result
    app.run(host='0.0.0.0', debug=True)
