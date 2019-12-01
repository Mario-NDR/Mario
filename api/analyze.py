from scapy.all import *
import time
def analyze_pcap(pcap_path):
    pcap_data = sniff(offline=pcap_path)
    analyze_result = []
    for i in range (len(pcap_data)):
        try:
            pcap_result = {}
            pcap_result['header'] = str(pcap_data[i][Raw].load,encoding="utf-8")
            pcap_result['src'] = pcap_data[i][IP].src
            pcap_result['dst'] = pcap_data[i][IP].dst
            analyze_result.append(pcap_result)
        except :
            pass
    return analyze_result
def analyze_iface(iface,count = 100):
    pcap_data = sniff(iface = "gif0", count = 100)
    # analyze_result = []
    # for i in range (len(pcap_data)):
    #     try:
    #         pcap_result = {}
    #         pcap_result['headers'] = str(pcap_data[i][Raw].load,encoding="utf-8")
    #         pcap_result['src'] = pcap_data[i][IP].src
    #         pcap_result['dst'] = pcap_data[i][IP].dst
    #         analyze_result.append(pcap_result)
    #     except :
    #         pass
    # return analyze_result