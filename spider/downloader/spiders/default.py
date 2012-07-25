#/bin/python

import time
from scrapy.spider import BaseSpider
from scrapy.conf import settings
from scrapy.stats import stats

from downloader.parsers.parsermw import ParserMiddlewareManager
from downloader.dal.product import ProductDAO

class DefaultSpider(BaseSpider):
    name = 'default_spider'

    def __init__(self, name, **kwargs):
        super(DefaultSpider, self).__init__(name, **kwargs)
        dbsettings = settings.get('MONGODB')
        self.productDao = ProductDAO(dbsettings)
        self.parser_manager = ParserMiddlewareManager.from_settings(settings, self)
        self.start_urls = []
        self.start_time = int(time.time())
        self.log("start spider %s" % self.name)

    def parse(self, response):
        self.log('Response:%s, type:%s' %(response.url, type(response)))
        self.parser_manager.process_response(response, self)

        stats.inc_value('crawled_url_num', spider=self)
        stats.inc_value('crawled_page_size', count=len(response.body), spider=self,)
