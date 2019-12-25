from scapy.all import *
from api.ip import ipAnalysis
import time
import json
import traceback
import random


def analyze_pcap(pcap_path):
    pcap_data = sniff(offline=pcap_path)
    result = {}
    analyze_result = []
    for i in range(len(pcap_data)):
        try:
            pcap_result = {}
            pcap_result['header'] = str(
                pcap_data[i][Raw].load, encoding="utf-8")
            pcap_result['src'] = pcap_data[i][IP].src
            pcap_result['dst'] = pcap_data[i][IP].dst
            analyze_result.append(pcap_result)
        except:
            pass
    result['data'] = analyze_result
    return result


def analyze_suricata(eve_json, data="ip", language="en"):
    eve_file = open(eve_json, "r")
    eve_lines = eve_file.readlines()
    eve_result = {}
    result = []
    if data == "ip":
        for eve_line in eve_lines:
            eve_info = {}
            eve_line = json.loads(eve_line)
            try:
                src = eve_line["src_ip"]+":"+str(eve_line["src_port"])
                dest = eve_line["dest_ip"]+":"+str(eve_line["dest_port"])
                event_type = eve_line["event_type"]
                alert_message = eve_line["alert"]["signature"]
                action = eve_line["alert"]["action"]
                if event_type == "alert":
                    eve_info["src"] = src
                    eve_info["dest"] = dest
                    eve_info["event_type"] = event_type
                    eve_info["alert_message"] = alert_message
                    eve_info["action"] = action
                    eve_info["src_count"] = random.randint(0,30)
                    eve_info["dest_count"] = random.randint(0,30)
                    if "DONE" in eve_info["alert_message"]:
                        eve_info["src"] = eve_info["dest"]
                        eve_info["dest"] = ipAnalysis.get_city(src, language)
                    result.append(eve_info)
            except:
                pass
    elif data == "city":
        for eve_line in eve_lines:
            eve_info = {}
            eve_line = json.loads(eve_line)
            try:
                src = eve_line["src_ip"]
                dest = eve_line["dest_ip"]
                event_type = eve_line["event_type"]
                alert_message = eve_line["alert"]["signature"]
                action = eve_line["alert"]["action"]
                if event_type == "alert":
                    eve_info["src"] = ipAnalysis.get_city(src, language)
                    eve_info["dest"] = ipAnalysis.get_city(dest, language)
                    eve_info["event_type"] = event_type
                    eve_info["alert_message"] = alert_message
                    eve_info["action"] = action
                    eve_info["src_count"] = random.randint(0,30)
                    eve_info["dest_count"] = random.randint(0,30)
                    if "DONE" in eve_info["alert_message"]:
                        eve_info["src"] = eve_info["dest"]
                        eve_info["dest"] = ipAnalysis.get_city(src, language)
                    result.append(eve_info)
            except:
                pass
    elif data == "xy":
        for eve_line in eve_lines:
            eve_info = {}
            eve_line = json.loads(eve_line)
            try:
                src = eve_line["src_ip"]
                dest = eve_line["dest_ip"]
                event_type = eve_line["event_type"]
                alert_message = eve_line["alert"]["signature"]
                action = eve_line["alert"]["action"]
                if event_type == "alert":
                    eve_info["src"] = ipAnalysis.get_city(
                        src, language, location=True)
                    eve_info["dest"] = ipAnalysis.get_city(
                        dest, language, location=True)
                    eve_info["event_type"] = event_type
                    eve_info["alert_message"] = alert_message
                    eve_info["action"] = action
                    eve_info["src_count"] = random.randint(0,30)
                    eve_info["dest_count"] = random.randint(0,30)
                    if "DONE" in eve_info["alert_message"]:
                        eve_info["src"] = eve_info["dest"]
                        eve_info["dest"] = ipAnalysis.get_city(src, language)
                    result.append(eve_info)
            except:
                pass
    eve_result['data'] = result
    return json.dumps(eve_result)
