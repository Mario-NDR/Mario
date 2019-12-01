
import geoip2.database
GeoipDatabase = geoip2.database.Reader('files/ipdb/GeoLite2-City.mmdb')
class ipAnalysis(object):
    def get_city(ip,language = "en",location = False):
        response_data = GeoipDatabase.city(ip)
        if location:
            try:
                return response_data.country.names[language],response_data.city.names[language],response_data.location.longitude,response_data.location.latitude
            except KeyError:
                return response_data.country.names[language],response_data.city.name,response_data.location.longitude,response_data.location.latitude
        else:
            try:
                return response_data.country.names[language],response_data.city.names[language]
            except KeyError:
                return response_data.country.names['en'],response_data.city.name
