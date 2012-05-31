#!/bin/python

import time
from scrapy import log

class HostPoliteCtrlMiddleware(object):
    HOST_POLITENESS_DELAY = 1.0
    REQ_SCHD_KEY = "reschd_key"

    def __init__(self):
        self.last_crawl_time = 0
        self.default_crawl_interval = 3 #second

    def process_request(self, request, spider):
        left_time = time.time() - self.last_crawl_time 
        
        if left_time < self.default_crawl_interval:
            wait_time = self.default_crawl_interval - left_time
            log.msg('Request[%s] wait %fs, for policy' % \
                (request.url, wait_time), level=log.DEBUG, spider=spider)
            time.sleep(wait_time)
  
        self.last_crawl_time = time.time()
