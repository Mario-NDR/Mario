import os
import api.analyze
from core.web import web_pcap_analyze
dir=os.environ.get(os.getcwd())
# print (api.ip.ipAnalysis.get_city('95.169.17.220'))
# print (api.ip.ipAnalysis.get_city('95.169.17.220',language='zh-CN',location=True))
# print (api.analyze.analyze_pcap('files/pcaps/thinkphp_5.x_rce_success.pcap'))
web_pcap_analyze('files/pcaps/cve_2017_7985_success.pcap',language="en",location=True)
