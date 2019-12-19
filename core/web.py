from api.analyze import analyze_pcap
from api.ip import ipAnalysis


def web_pcap_analyze(pcap, language="en", location=False):
    analyze_result = analyze_pcap(pcap)
    for result in analyze_result:
        headers = result['header']
        # print (result['src'],result['dst'])
        if location == False:
            try:
                ipsrc = ipAnalysis.get_city(result['src'], language)
            except:
                ipsrc = result['src']
            try:
                ipdst = ipAnalysis.get_city(result['dst'], language)
            except:
                ipdst = result['dst']
        else:
            try:
                ipsrc = ipAnalysis.get_city(
                    result['src'], language, location=True)
            except:
                ipsrc = result['src']
            try:
                ipdst = ipAnalysis.get_city(
                    result['dst'], language, location=True)
            except:
                ipdst = result['dst']
        if type(ipsrc) is tuple:
            ipsrc_info = {}
            ipsrc_info['country'] = ipsrc[0]
            ipsrc_info['city'] = ipsrc[1]
            try:
                ipsrc_info['location'] = ipsrc[2]
            except:
                pass
            ipsrc = ipsrc_info
        if type(ipdst) is tuple:
            ipdst_info = {}
            ipdst_info['country'] = ipdst[0]
            ipdst_info['city'] = ipdst[1]
            try:
                ipdst_info['location'] = ipdst[2]
            except:
                pass
            ipdst = ipdst_info
        print(ipsrc, ipdst)
