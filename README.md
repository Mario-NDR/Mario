# Mario · ![](https://img.shields.io/github/license/Mario-NDR/Mario)
Mario 流量分析框架

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

- 演示地址：

  [蔚蓝盾](http://fenglipaipai.xyz)

## 服务端部署：
```bash
docker-compose up --build -d 
or 
bash build.sh
```
访问：
http://127.0.0.1:9955 登录界面  

### 前端静态文件
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
如果 ping 不同则表示成功部署
## 使用方法
- web（后端）：
```python
python3 run.py
```
## 前端接口文档
- 威胁情报地图模块 （http://127.0.0.1:5000/api/map）

使用`GET`方法设置时间范围`http://127.0.0.1:5000/map?begintime=2019-08-13T20:52:58+0000&endtime=2019-08-23T20:52:58+0000`获取时间段内的数据

- 还有好多，懒得写了
