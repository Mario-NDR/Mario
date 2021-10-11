from elasticsearch import Elasticsearch
import configparser

def insert_es(index_name,value=None):
    config = configparser.ConfigParser()
    config.read('config.cfg')
    if config['elastic']['pass'] and config['elastic']['user']:
        es = Elasticsearch(["{}:{}".format(config['elastic']['host'],config['elastic']['port'])],http_auth="{}:{}".format(config['elastic']['user'],config['elastic']['pass']))
    else:
        es = Elasticsearch(["{}:{}".format(config['elastic']['host'],config['elastic']['port'])])
    if value == None:
        es.indices.create(index_name, ignore=400)
    else:
        es.index(index_name,body=value)
def search_es(index_name,begintime=None,endtime=None,limit=None):
    config = configparser.ConfigParser()
    config.read('config.cfg')
    if config['elastic']['pass'] and config['elastic']['user']:
        es = Elasticsearch(["{}:{}".format(config['elastic']['host'],config['elastic']['port'])],http_auth="{}:{}".format(config['elastic']['user'],config['elastic']['pass']))
    else:
        es = Elasticsearch(["{}:{}".format(config['elastic']['host'],config['elastic']['port'])])
    es_search_body = {
        "query": {
            "bool": {
                "must": [],
                "filter": [
                    {
                        "match_all": {}
                    },
                    {
                        "exists": {
                            "field": "alert.category.keyword"
                        }
                    },
                    {
                        "range": {
                            "timestamp": {
                                "gte": begintime,
                                "lte": endtime,
                                "format": "strict_date_optional_time"
                            }
                        }
                    }
                ],
                "should": [],
                
            }
        }
    }
    print(es_search_body)
    es_search_result = es.search(
                index=index_name, body=es_search_body, size=limit)
    return es_search_result['hits']['hits']
def get_all_index():
    config = configparser.ConfigParser()
    config.read('config.cfg')
    if config['elastic']['pass'] and config['elastic']['user']:
        es = Elasticsearch(["{}:{}".format(config['elastic']['host'],config['elastic']['port'])],http_auth="{}:{}".format(config['elastic']['user'],config['elastic']['pass']))
    else:
        es = Elasticsearch(["{}:{}".format(config['elastic']['host'],config['elastic']['port'])])
    result = []
    for key in es.indices.get_alias().keys():
        result_detil = {}
        if any(_ == key for _ in ['http','dns','fileinfo','tls']):
            result_detil['name'] = key
            result_detil['count'] = es.count(index=key)['count']
            result.append(result_detil)
        else:
            continue
        # if any(_ in key for _ in ['alert', 'stats','.','_']):
        #     continue
        # else:
        #     result_detil['name'] = key
        #     result_detil['count'] = es.count(index=key)['count']
        #     result.append(result_detil)
    return result
