#/bin/python

from scrapy.spider import BaseSpider
from scrapy.conf import settings

from slave.parsers.parsermw import ParserMiddlewareManager
from slave.dao.goods_dao import GoodsDAO

class BasicSpider(BaseSpider):
    name = 'basicspider'

    def __init__(self):
        mongodb_host = settings.get('MONGODB_HOST') 
        mongodb_port = settings.get('MONGODB_PORT')
        mongodb_dbname = settings.get('MONGODB_DBNAME')
        default_collection = settings.get('DEFAULT_COLLECTION_NAME')
        self.dbclient = GoodsDAO(mongodb_host, mongodb_port, 
            mongodb_dbname, default_collection)
        self.parser_manager = ParserMiddlewareManager.from_settings(settings, self)
        self.start_urls = []
        self.log("start spider %s" % self)

    def parse(self, response):
        self.parser_manager.process_response(response)
