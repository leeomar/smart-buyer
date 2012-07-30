#/bin/python
from downloader.utils.url import get_domain
from downloader.utils.timecmp import today
from downloader.clients.myredis import MyRedisClient

class StatisticInfo(object):
    EXTRACT_LINK_OK = 'LINK_OK'
    EXTRACT_LINK_FAIL = 'LINK_FAIL'

    RECORD_SAVED = 'RECORD_SAVED'
    RECORD_EXTRACTED = 'RECORD_EXTRACTED'

    def __init__(self, redis_settings):
        self.redis = MyRedisClient.from_settings(redis_settings) 

    def genkey(self, suffix, strtime=None):
        return "%s:%s" % (strtime if strtime else today(), suffix)

    def save_extract_info(self, url, item_num):
        if item_num > 0:
            domain = get_domain(url)
            self.redis.hincrby(self.genkey(self.EXTRACT_LINK_OK), domain, item_num)
        else:
            self.redis.sadd(self.genkey(self.EXTRACT_LINK_FAIL), url)
    
    def get_extract_info(self, strtime):
        return self.redis.hgetall(self.genkey(self.EXTRACT_LINK_OK, strtime))

    def get_error_info(self, strtime):
        return self.redis.smembers(self.genkey(self.EXTRACT_LINK_FAIL, strtime))

    def record_saved(self, record):
        self.redis.hincrby(self.genkey(self.RECORD_SAVED), record['domain'], 1)

    def record_extracted(self, record):
        self.redis.hincrby(self.genkey(self.RECORD_EXTRACTED), record['domain'], 1)

    def get_record_saved(self, strtime):
        return self.redis.hgetall(self.genkey(self.RECORD_SAVED, strtime))

    def get_record_extracted(self,strtime):
        return self.redis.hgetall(self.genkey(self.RECORD_EXTRACTED, strtime))
