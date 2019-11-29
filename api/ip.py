# import geoip2.database
# GeoipDatabase = geoip2.database.Reader('GeoLite2-City.mmdb')
# response_data = GeoipDatabase.city('97.132.182.78')
# # 获取经纬度
# longitude = response_data.location.longitude
# latitude = response_data.location.latitude
# # 城市名称
# cityname = response_data.city.name
# # 国家名称
# country = response_data.country.name
# print (country,cityname,longitude,latitude)

# GeoipDatabase.close()
import geoip2.database
GeoipDatabase = geoip2.database.Reader('files/GeoLite2-City.mmdb')
class ipAnalysis(object):
    def get_city(ip,language = "en"):
        response_data = GeoipDatabase.city(ip)
        try:
            return response_data.country.names[language],response_data.city.names[language]
        except :
            return response_data.country.names['en'],response_data.city.names['en']
    def get_location(ip):
        response_data = GeoipDatabase.city(ip)
        return response_data.location.longitude,response_data.location.latitude
