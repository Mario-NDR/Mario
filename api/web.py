import os
import time
import api.analyze
from flask import redirect,url_for
ALLOW_EXTENSIONS = ['pcap','pcapng']
UPLOAD_PATH = "files/pcaps"
def check_pcapname(filename):
    if any(filename.split(".")[1] in _ for _ in ALLOW_EXTENSIONS):
        return filename
def map():
    result = api.analyze.analyze_suricata("files/suricata/eve.json",data="xy",language="en")
    return str(result)
def ip():
    ipResult = api.analyze.analyze_suricata("files/suricata/eve.json",data="ip",language="en")
    return str(ipResult)
def upload_pcap(file):
    filename = file.filename
    if check_pcapname(filename):
        file.save(os.path.join(UPLOAD_PATH, filename))
        redirect(url_for('upload_file',filename=filename))
        return "上传成功",2000
    else:
        return "上传文件格式不正确，请上传 pcap 或 pcapng ",2001
def analyze_pcap(filename):
    if check_pcapname(filename):
        analyzefile = os.path.join(UPLOAD_PATH,filename)
        result = api.analyze.analyze_pcap(analyzefile)
        return result
    else:
        return "数据包不存在",2002