
from lib.data import config
import geoip2.database
import requests
import re
GeoipDatabase = geoip2.database.Reader('files/ipdb/GeoLite2-City.mmdb')
class ipAnalysis(object):
    def get_city(ip,language = "en",location = False):
        try:
            response_data = GeoipDatabase.city(ip)
        except geoip2.errors.AddressNotFoundError:
            # ip = re.findall(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b",requests.get("http://myip.ipip.net").text)
            # config['ip'] = ip
            ip = "58.132.182.78"
            response_data = GeoipDatabase.city(ip)
        if location:
            try:
                ip_info = {}
                ip_info["country"] = response_data.country.names[language]
                ip_info["city"] = response_data.city.names[language]
                ip_info["longitude"] = response_data.location.longitude
                ip_info["latitude"] = response_data.location.latitude
                return ip_info# return response_data.country.names[language],response_data.city.names[language],response_data.location.longitude,response_data.location.latitude
            except KeyError:
                return response_data.country.names[language],response_data.city.name,response_data.location.longitude,response_data.location.latitud
                ip_info = {}
                ip_info["country"] = response_data.country.names[language]
                ip_info["city"] = response_data.city.name
                ip_info["longitude"] = response_data.location.longitude
                ip_info["latitude"] = response_data.location.latitude
                return ip_info
        else:
            try:
                ip_info = {}
                ip_info["country"] = response_data.country.names[language]
                ip_info["city"] = response_data.city.names[language]
                return ip_info
            except KeyError:
                ip_info = {}
                ip_info["country"] = response_data.country.names[language]
                ip_info["city"] = response_data.city.name
                return ip_info
    def get_local_ip():
        ip = re.findall(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b",requests.get("http://myip.ipip.net").text)
        return ip