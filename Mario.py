import os
import sys
import api.analyze
from api.ip import ipAnalysis
from lib.data import config
from core.webserver import webserver


def check_env():
    config['ip'] = ipAnalysis.get_local_ip()


def start():
    if get_mod() == "python":
        results = api.analyze.analyze_suricata(
            "files/suricata/eve.json", data="xy", language="en")
        print(results)
    elif get_mod() == "web":
        webserver()


def get_mod():
    if len(sys.argv) == 2:
        return "web"
    else:
        return "python"


if __name__ == "__main__":
    check_env()
    start()
