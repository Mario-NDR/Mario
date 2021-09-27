import os
import json
import sys
import api.analyze
from api.ip import ipAnalysis
from core.webserver import webserver
from run import app


def start():
    if get_mod() == "python":
        results = api.analyze.analyze_suricata_alert(data="xy", language="en")
    elif get_mod() == "web":
        webserver()


def get_mod():
    if len(sys.argv) == 2:
        return "web"
    else:
        return "python"


if __name__ == "__main__":
    start()
