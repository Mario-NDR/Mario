import os
import api.ip
dir=os.environ.get(os.getcwd())
print (api.ip.ipAnalysis.get_city('95.169.17.220'))
# print (api.ip.ipAnalysis.get_city('95.169.17.220',language='zh-CN',location=True))


