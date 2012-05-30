"""
HostPoliteCtrlMiddleware is a downloader middleware to handle host politeness
"""

import string

#from urlparse import urlparse
import time
from scrapy.utils.httpobj import urlparse_cached
from twisted.internet import reactor, defer
from scrapy.http import Request
from scrapy.core.engine import ExecutionEngine
from scrapy.conf import settings
from scrapy.project import crawler
from scrapy.crawler import Crawler
from scrapy.exceptions import IgnoreRequest
from scrapy import log


class HostPoliteCtrlMiddleware(object):

    HOST_POLITENESS_DELAY = 1.0
    REQ_SCHD_KEY = "reschd_key"

    def __init__(self):
        #site_crawl_delay_file = settings.get('SITE_CRAWL_DELAY_MAP')
        #self._site_crawl_delay_map['default'] = self.HOST_POLITENESS_DELAY 
        self.last_crawl_time = 0
        self.default_crawl_interval = 3 #second

    def process_request(self, request, spider):
        left_time = time.time() - self.last_crawl_time 
        
        if left_time < self.default_crawl_interval:
            wait_time = self.default_crawl_interval - left_time
            log.msg('Request[%s] wait %fs, for policy' % (request.url, wait_time), level=log.DEBUG, spider=spider)
            time.sleep(wait_time)
  
        self.last_crawl_time = time.time()
        #return request
