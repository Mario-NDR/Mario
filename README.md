# Mario · ![](https://img.shields.io/github/license/Mario-NDR/Mario)
Mario 流量分析框架
一旦使用本开源项目以及引用了本项目或包含本项目代码的公司因为违反劳动法（包括但不限定非法裁员、超时用工、雇佣童工等）在任何法律诉讼中败诉的，项目作者有权利追讨本项目的使用费，或者直接不允许使用任何包含本项目的源代码！任何性质的外包公司或996公司需要使用本类库，请联系作者进行商业授权！其他企业或个人可随意使用不受限。(复制自 https://github.com/ldqk/Masuit.Tools )
## 项目说明

- [Mario 流量分析框架 ](https://github.com/Mario-NDR/Mario/)+ [Peach 前端框架](https://github.com/Mario-NDR/Peach) = [蔚蓝盾入侵检测系统](https://github.com/Mario-NDR/)

  主要源码在 github 开源，gitee 中的代码是为了方便国内服务器部署，喜欢的话请顺手 star github 的仓库

- 项目初衷：

  部分一线安全厂商入侵检测系统使用的均为魔改后的 suricata 或 snort，我们的项目不会做的像几百人团队的产品一样的流畅和完美， 只是为了向大家普及入侵检测系统

- 维护更新计划：

  毕设结束后，我们会在工作之余更新代码，迭代新的功能

- 入侵检测规则：

  基于 suricata 语法的入侵检测规则，重大安全漏洞均会更新

- 版权：

  我们的项目永久开源，大家可以随便使用，请勿用于商业用途

## 展示

!(mario_map.png)[./photos/mario_map.png]  
!(mario_ana.png)[./photos/mario_ana.png]  
!(mario_alert.png)[./photos/mario_alert.png]  
!(mario_alert_detil.png)[./photos/mario_alert_detil.png]  
!(mario_virtual.png)[./photos/mario_virtual.png]  


## 服务端部署：
```bash
docker-compose up --build -d 
or 
bash build.sh
```
访问：
http://127.0.0.1:9955 登录界面

### 前端静态文件 (非二开不用看)
`ThirPath/web`  
获取最新前端静态文件方法  
`curl https://api.github.com/repos/Mario-NDR/Peach/releases/latest | sed -r -n 's/.*"browser_download_url": *"(.*)".*/\1/p' | wget -q -i -`

## 客户端部署（暂仅支持ubuntu）
测试连通性:
```bash
ping ip
```
部署客户端
```bash
curl ip:5000/install.sh | bash
```
下发 ICMP test 拦截规则  
测试安装是否成功  
```bash
ping ip
```
如果 ping 不通则表示成功部署

## 使用方法 （非二开不用看）
- web（后端）：
```python
python3 run.py
```
