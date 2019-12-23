# Mario
Mario 流量分析框架
# ip 信息分析 api
分析 ip 所在位置（国家，城市，经纬度）
## 使用方法
- 命令行模式：
```python
python3 Mario.py
```
- web模式（无前端）：
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

## 前端接口文档
- 流量包上传模块 （http://127.0.0.1:5000/upload）
使用 POST 方式上传流量包 （pcap，pcapng）
状态码：
2000 ：流量包上传成功
2001 ：流量包格式错误
- 流量包解析模块（http://127.0.0.1:5000/pcap）
使用 POST 方式传递需要解析的流量包的名称
状态码：
2002 ： 流量包不存在
- 威胁情报地图模块 （http://127.0.0.1:5000/map）
- 攻击流量（ip）显示模块（http://127.0.0.1:5000/ip）
## 整体展示：
```bash
docker build -t mario .
docker run -it -p 9955:9955 -p 5000:5000 -d mario
```
访问：
http://127.0.0.1:9955/app/map


