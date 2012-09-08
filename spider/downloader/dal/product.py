#/bin/python
# -*- coding: utf-8 -*-

from scrapy.utils.signal import send_catch_log
from scrapy import log

from downloader import signals
from downloader.utils.url import get_uid
from downloader.clients.mymongo import MongoClient
from .record import ProductRecord
    
class ProductDAO:

    def __init__(self, dbsettings):
        self.mongo = MongoClient.from_settings(dbsettings)
        self.mongo.open()

    def get(self, url, collection_name=None):
        uid = get_uid(url)
        dbrecord = self.mongo.find_one(uid, collection_name)
        if dbrecord:
            record = ProductRecord()
            record.oid = str(dbrecord['_id'])
            record.url = dbrecord['url']
            record.uid = dbrecord['uid']
            record.name = dbrecord['name']
            record.cat = dbrecord['cat']
            record.data = dbrecord['data']
            record.bottom_price = dbrecord['bottom_price']
            record.domain = dbrecord['domain']
            return record
        else:
            return None

    def put(self, record, collection_name):
        uid = record['uid'] 
        url = record['url']
        dbrecord = self.get(url, collection_name)
        if dbrecord:
            price = record['data'][0][0]
            crawltime = record['data'][0][1]
            if dbrecord.add_price(price, crawltime):
                self.mongo.update_field(
                    uid, collection_name, 
                    data=dbrecord.data,
                    bottom_price=dbrecord.bottom_price)
            else:
                log.msg('duplicate price, uid:%s, url:%s' % (uid, url))
                return
        else: 
            self.mongo.insert(record, uid, collection_name)
        log.msg("save record: %s" % record)
        send_catch_log(signal=signals.product_record_saved, record=record)

if __name__ == '__main__':
    productDAO = ProductDAO('127.0.0.1', 27017, "test", "test")
    url = 'http://www.360buy.com/product/342079.html'
    name = "moto手机"
    cat = "手机"
    price = 1599

    productDAO.put(url, name, cat, price)
    price = 1498
    productDAO.put(url, name, cat, price)
