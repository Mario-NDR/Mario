# Mario
Mario 流量分析框架
# ip 信息分析 api
分析 ip 所在位置（国家，城市，经纬度）
## 使用方法
- 命令行模式：
```python
python3 Mario.py
```
- web模式（无后端）：
```python
python3 Mario.py web
```
## python 方法调用方法
- 根据 IP 获得城市信息  
api.ip.ipAnalysis.get_city('95.169.17.220')
- 获取中文城市信息，及坐标信息  
api.ip.ipAnalysis.get_city('95.169.17.220',language='zh-CN',location=True)
- 通过流量包分析  
api.analyze.analyze_pcap('files/pcaps/thinkphp_5.x_rce_success.pcap')
web_pcap_analyze('files/pcaps/cve_2017_7985_success.pcap',language="en",location=True)
- 通过 suricata 告警信息分析  
api.analyze.analyze_suricata("files/suricata/eve.json",data="ip")