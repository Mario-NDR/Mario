import os
import api.analyze
from api.ip import ipAnalysis
from lib.data import config
from core.web import web_pcap_analyze

def check_env():
    # dir=os.environ.get(os.getcwd())
    config['ip'] = ipAnalysis.get_local_ip()
def start():
    results = api.analyze.analyze_suricata("files/suricata/eve.json",data="xy",language="en")
    for result in results:
        print (result)
if __name__ == "__main__":
    check_env()
    start()