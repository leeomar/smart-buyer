#/bin/python
from crawler.utils.url import get_domain
from crawler.utils.time import today
from crawler.clients.myredis import MyRedisClient

class GoodsMetaInfo(object):
    EXTRACT_ITEM_OK = 'OK'
    EXTRACT_ITEM_FAIL = 'FAIL'

    def __init__(self, redis_settings):
        self.redis = MyRedisClient.from_settings(redis_settings) 

    def genkey(self, suffix, strtime=None):
        return "%s:%s" % (strtime if strtime else today(), suffix)

    def save_extract_info(self, url, item_num):
        if item_num > 0:
            domain = get_domain(url)
            self.redis.hincrby(self.genkey(self.EXTRACT_ITEM_OK), domain, item_num)
        else:
            self.redis.sadd(self.genkey(self.EXTRACT_ITEM_FAIL), url)

    def get_extract_info(self, strtime):
        return self.redis.hgetall(self.genkey(self.EXTRACT_ITEM_OK, strtime))

    def get_error_info(self, strtime):
        return self.redis.smembers(self.genkey(self.EXTRACT_ITEM_FAIL, strtime))
