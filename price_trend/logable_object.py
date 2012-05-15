#/bin/python

from scrapy import log

class LogableObject(object):
    
    def __init__(self, spider=None):
        self.spider = spider 
    
    def log(msg, level=log.DEBUG, spider=None)
        if spider is None:
            spider = self.spider
        log.msg(msg, level=level, spider=spider)
