import os
import lib.data
import api.ip
#print (os.getcwd())
dir=os.environ.get(os.getcwd())
print (api.ip.ipAnalysis.get_city('95.169.17.220'))
# print (api.ip.ipAnalysis.get_city('95.169.17.220',language='zh-CN'))
print (api.ip.ipAnalysis.get_location('95.169.17.220'))

