from scapy.all import *
from lib.data import config, src_ip, dest_ip
from api.ip import ipAnalysis
from api.mongo import findeve, evetomongo
from bson import json_util
from api.logger import logger
from datetime import timedelta
from api.autorules import generate_by_ip
import re
import time
import json
import traceback
import random
import traceback


def analyze_suricata_alert(data="xy", language="en", begintime=None, endtime=None):
    src_ip.clear()
    dest_ip.clear()
    eve_result = {}
    result = []
    eve_lines = findeve("alert", begintime, endtime)
    if begintime != None and endtime != None:
        for eve_line in eve_lines:
            eve_info = {}
            eve_line = json_util.dumps(eve_line)
            eve_line = json.loads(eve_line)
            try:
                src = eve_line["src_ip"]
                dest = eve_line["dest_ip"]
                proto = eve_line["proto"]
                event_type = eve_line["event_type"]
                alert_message = eve_line["alert"]["signature"]
                try:
                    category = eve_line["alert"]["category"]
                except:
                    category = "None"
                action = eve_line["alert"]["action"]
                if event_type == "alert":
                    eve_info["time"] = eve_line["timestamp"]
                    if ipAnalysis.is_internal_ip(src) or re.findall(r'^127\.', src):
                        if ipAnalysis.is_internal_ip(eve_line['client_ip']) or re.findall(r'^127\.', eve_line['client_ip']):
                            try:
                                eve_info["src"] = ipAnalysis.get_city(
                                    config['ip'][0], language, location=True)
                            except:
                                eve_info["src"] = ipAnalysis.get_city(
                                    config['ip'][0], language='en', location=True)
                        else:
                            try:
                                eve_info["src"] = ipAnalysis.get_city(
                                    eve_line['client_ip'], language, location=True)
                            except:
                                eve_info["src"] = ipAnalysis.get_city(
                                    eve_line['client_ip'], language='en', location=True)
                        eve_info["src"]["ip"] = src
                    else:
                        if "联防-自学习" not in alert_message:
                            generate_by_ip(src)
                        try:
                            eve_info["src"] = ipAnalysis.get_city(
                                src, language, location=True)
                        except:
                            eve_info["src"] = ipAnalysis.get_city(
                                src, language='en', location=True)
                    if ipAnalysis.is_internal_ip(dest) or re.findall(r'^127\.', dest):
                        if ipAnalysis.is_internal_ip(eve_line['client_ip']) or re.findall(r'^127\.', eve_line['client_ip']):
                            try:
                                eve_info["dest"] = ipAnalysis.get_city(
                                    config['ip'][0], language, location=True)
                            except:
                                eve_info["dest"] = ipAnalysis.get_city(
                                    config['ip'][0], language='en', location=True)
                        else:
                            try:
                                eve_info["dest"] = ipAnalysis.get_city(
                                    eve_line['client_ip'], language, location=True)
                            except:
                                eve_info["dest"] = ipAnalysis.get_city(
                                    eve_line['client_ip'], language='en', location=True)
                        eve_info["dest"]["ip"] = dest
                    else:
                        try:
                            eve_info["dest"] = ipAnalysis.get_city(
                                dest, language, location=True)
                        except:
                            eve_info["dest"] = ipAnalysis.get_city(
                                dest, language='en', location=True)
                    if proto == "UDP":
                        try:
                            eve_info["dest"]["ip"] = eve_line['dns']['query'][0]['rrname']
                        except:
                            eve_info["dest"]["ip"] = eve_info["dest"]["ip"]
                    try:
                        eve_info["src"]["src_port"] = eve_line["src_port"]
                    except Exception as e:
                        eve_info["src"]["src_port"] = "ICMP or UDP"

                    try:
                        eve_info["dest"]["dest_port"] = eve_line["dest_port"]
                    except Exception as e:
                        eve_info["dest"]["dest_port"] = "ICMP or UDP"
                    eve_info["event_type"] = event_type
                    eve_info["client_ip"] = eve_line['client_ip']
                    eve_info["alert_message"] = alert_message
                    eve_info["category"] = category
                    eve_info["action"] = action
                    try:
                        src_ip[eve_info["src"]["ip"]] += 1
                    except:
                        src_ip[eve_info["src"]["ip"]] = 1
                    try:
                        dest_ip[eve_info["dest"]["ip"]] += 1
                    except:
                        dest_ip[eve_info["dest"]["ip"]] = 1
                    result.append(eve_info)
            except Exception as e:
                print("error {}".format(e))
                pass
    else:
        for eve_line in eve_lines:
            eve_info = {}
            eve_line = json_util.dumps(eve_line)
            eve_line = json.loads(eve_line)
            try:
                src = eve_line["src_ip"]
                dest = eve_line["dest_ip"]
                proto = eve_line["proto"]
                event_type = eve_line["event_type"]
                alert_message = eve_line["alert"]["signature"]
                try:
                    category = eve_line["alert"]["category"]
                except:
                    category = "None"
                action = eve_line["alert"]["action"]
                if event_type == "alert":
                    eve_info["time"] = eve_line["timestamp"]
                    eve_info["src"] = {}
                    eve_info["src"]["ip"] = src
                    if ipAnalysis.is_internal_ip(src) or re.findall(r'^127\.', src):
                        print("内网威胁{}".format(src))
                    else:
                        if "联防-自学习" not in alert_message:
                            generate_by_ip(src)
                    eve_info["dest"] = {}
                    eve_info["dest"]["ip"] = dest
                    if proto == "UDP":
                        try:
                            eve_info["dest"]["ip"] = eve_line['dns']['query'][0]['rrname']
                        except:
                            eve_info["dest"]["ip"] =eve_info["dest"]["ip"]
                    try:
                        eve_info["src"]["src_port"] = eve_line["src_port"]
                    except Exception as e:
                        eve_info["src"]["src_port"] = "ICMP or UDP"

                    try:
                        eve_info["dest"]["dest_port"] = eve_line["dest_port"]
                    except Exception as e:
                        eve_info["dest"]["dest_port"] = "ICMP or UDP"
                    eve_info["event_type"] = event_type
                    eve_info["client_ip"] = eve_line['client_ip']
                    eve_info["alert_message"] = alert_message
                    eve_info["category"] = category
                    eve_info["action"] = action
                    try:
                        src_ip[eve_info["src"]["ip"]] += 1
                    except:
                        src_ip[eve_info["src"]["ip"]] = 1
                    try:
                        dest_ip[eve_info["dest"]["ip"]] += 1
                    except:
                        dest_ip[eve_info["dest"]["ip"]] = 1
                    result.append(eve_info)
            except Exception as e:
                print("error {}".format(e))
                print(eve_line)
                pass
    for eve_info in result:
        eve_info["src"]["src_count"] = src_ip[eve_info["src"]["ip"]]
        eve_info["dest"]["dest_count"] = dest_ip[eve_info["dest"]["ip"]]
    eve_result['data'] = result[::-1]
    eve_result["infonum"] = len(result)
    return eve_result


def analyze_to_wavy(begintime=None, endtime=None):
    def gen_dates(b_date, days):
        day = timedelta(days=1)
        for i in range(days):
            yield b_date + day*i
    eve_lines = findeve("alert", begintime, endtime)
    date_span = gen_dates(datetime.strptime(begintime, "%Y-%m-%dT%z"), (datetime.strptime(
        endtime, "%Y-%m-%dT%H:%M:%S%z")-datetime.strptime(begintime, "%Y-%m-%dT%z")).days+1)
    days = []
    for date in date_span:
        days.append(datetime.strftime(date, "%Y-%m-%d"))
    return eve_lines, days
