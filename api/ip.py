
import geoip2.database
GeoipDatabase = geoip2.database.Reader('files/GeoLite2-City.mmdb')
class ipAnalysis(object):
    def get_city(ip,language = "en",location = False):
        response_data = GeoipDatabase.city(ip)
        if location:
            try:
                return response_data.country.names[language],response_data.city.names[language],response_data.location.longitude,response_data.location.latitude
            except :
                return response_data.country.names['en'],response_data.city.names['en'],response_data.location.longitude,response_data.location.latitude
        else:
            try:
                return response_data.country.names[language],response_data.city.names[language]
            except :
                return response_data.country.names['en'],response_data.city.names['en']
