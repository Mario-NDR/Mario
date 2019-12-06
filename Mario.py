import os
import api.analyze
from api.ip import ipAnalysis
from lib.data import config
from core.web import web_pcap_analyze

def check_env():
    dir=os.environ.get(os.getcwd())
    config['ip'] = ipAnalysis.get_local_ip()
result = api.analyze.analyze_suricata("files/suricata/eve.json",data="ip2")
print (result)
if __name__ == "__main__":
    check_env()