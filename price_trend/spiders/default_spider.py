#/bin/python

from scrapy.spider import BaseSpider
from scrapy.conf import settings

from price_trend.spiders.parser_manger import ParserManager
from price_trend.spiders.basic_parser import BasicLinkInfo
from price_trend.dao.goods_dao import GoodsDAO

class DefaultSpider(BaseSpider):

    def __init__(self):
        self.parser_manager=ParserManager.from_settings(settings, self)
        mongodb_host = settings.get('MONGODB_HOST') 
        mongodb_port = settings.get('MONGODB_PORT')
        mongodb_dbname = settings.get('MONGODB_DBNAME')
        default_collection = settings.get('DEFAULT_COLLECTION_NAME')
        self.goods_dao_ins = GoodsDAO(mongodb_host, mongodb_port, 
            mongodb_dbname, default_collection)

    def parse(self, response):
        self.parser_manager.process_response(response
