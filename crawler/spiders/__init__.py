#/bin/python

import time
from scrapy.spider import BaseSpider
from scrapy.conf import settings
from scrapy.stats import stats

from crawler.parsers.parsermw import ParserMiddlewareManager
from crawler.dal.goods import GoodsClient

class DefaultSpider(BaseSpider):
    #name = 'basicspider'
    def __init__(self, name, **kwargs):
        super(DefaultSpider, self).__init__(name, **kwargs)
        mongodb_host = settings.get('MONGODB_HOST') 
        mongodb_port = settings.get('MONGODB_PORT')
        mongodb_dbname = settings.get('MONGODB_DBNAME')
        default_collection = settings.get('DEFAULT_COLLECTION_NAME')
        self.dbclient = GoodsClient(mongodb_host, mongodb_port, 
            mongodb_dbname, default_collection)
        self.parser_manager = ParserMiddlewareManager.from_settings(settings, self)
        self.start_urls = []
        self.start_time = int(time.time())
        self.log("start spider %s" % self.name)

    def parse(self, response):
        self.log('Response:%s, type:%s' %(response.url, type(response)))
        self.parser_manager.process_response(response, self)

        stats.inc_value('crawled_url_num', spider=self)
        stats.inc_value('crawled_page_size', count=len(response.body), spider=self,)
