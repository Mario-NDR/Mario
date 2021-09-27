
import traceback
import geoip2.database
import requests
from api.logger import logger
import re
from functools import reduce
GeoipDatabase = geoip2.database.Reader('files/ipdb/GeoLite2-City.mmdb')
logger=logger
class ipAnalysis(object):
    def get_city(ip, language="en", location=False):
        try:
            response_data = GeoipDatabase.city(ip)
        except geoip2.errors.AddressNotFoundError:
            original_ip = ip
            response_data = GeoipDatabase.city(ipAnalysis.get_local_ip()[0])
            logger.warning("本地客户端内网遭到攻击")
        if location:
            try:
                ip_info = {}
                try:
                    ip_info["ip"] = original_ip
                except:
                    ip_info["ip"] = ip
                ip_info["country"] = response_data.country.names[language]
                ip_info["city"] = response_data.city.names[language]
                ip_info["longitude"] = response_data.location.longitude
                ip_info["latitude"] = response_data.location.latitude
                return ip_info
            except KeyError:
                ip_info = {}
                try:
                    ip_info["ip"] = original_ip
                except:
                    ip_info["ip"] = ip
                ip_info["country"] = response_data.country.names[language]
                ip_info["city"] = response_data.city.name
                if ip_info["city"] == None:
                    ip_info["city"] = ip_info["country"]
                ip_info["longitude"] = response_data.location.longitude
                ip_info["latitude"] = response_data.location.latitude
                return ip_info
        else:
            try:
                ip_info = {}
                try:
                    ip_info["ip"] = original_ip
                except:
                    ip_info["ip"] = ip
                ip_info["country"] = response_data.country.names[language]
                ip_info["city"] = response_data.city.names[language]
                return ip_info
            except KeyError:
                ip_info = {}
                ip_info["country"] = response_data.country.names[language]
                ip_info["city"] = response_data.city.name
                return ip_info

    def get_local_ip():
        ip = re.findall(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b",
                        requests.get("http://myip.ipip.net").text)
        return ip

    def is_internal_ip(ip_str):
        def ip_into_int(ip):
            return reduce(lambda x, y: (x << 8) + y, map(int, ip.split('.')))
        ip_int = ip_into_int(ip_str)
        net_A = ip_into_int('10.255.255.255') >> 24
        net_B = ip_into_int('172.31.255.255') >> 20
        net_C = ip_into_int('192.168.255.255') >> 16
        net_ISP = ip_into_int('100.127.255.255') >> 22
        net_DHCP = ip_into_int('169.254.255.255') >> 16
        return ip_int >> 24 == net_A or ip_int >> 20 == net_B or ip_int >> 16 == net_C or ip_int >> 22 == net_ISP or ip_int >> 16 == net_DHCP
