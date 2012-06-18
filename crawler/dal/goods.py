#/bin/python
# -*- coding: utf-8 -*-

from scrapy.utils.signal import send_catch_log
from scrapy import log

from crawler import signals
from crawler.utils.url import get_uid, get_domain
from .mymongo import MongoClient
from .item import GoodsItem
import time
    
class GoodsClient:

    def __init__(self, dbsettings):
        self.dbclient = MongoClient.from_settings(dbsettings)
        self.dbclient.open()

    def get(self, url, collection_name=None):
        uid = get_uid(url)
        dbrecord = self.dbclient.find_one(uid, collection_name)
        if dbrecord:
            item = GoodsItem()
            item.oid = str(dbrecord['_id'])
            item.url = dbrecord['url']
            item.uid = dbrecord['uid']
            item.name = dbrecord['name']
            item.cat = dbrecord['cat']
            item.data = dbrecord['data']
            item.bottom_price = dbrecord['bottom_price']
            item.domain = dbrecord['domain']
            return item
        else:
            return None
    
    def put(self, url, name, cat, price, collection_name=None):
        uid = get_uid(url)
        domain = get_domain(url)
        crawl_time = int(time.time()) 
        item = self.get(url, collection_name)
        if item:
            if item.add_price(price, crawl_time):
                self.dbclient.update_field(uid, collection_name, 
                    data=item.data,
                    bottom_price=item.bottom_price)
            else:
                log.msg('duplicate price')
                return
        else: 
            item = {   "url":url, 'uid': uid,  "name":name, 
                    "cat":cat, "data":[(price, crawl_time)], 
                    "bottom_price":(price, crawl_time), 
                    "domain":domain
                 }
            self.dbclient.insert(item, uid, collection_name)

        send_catch_log(signal=signals.item_saved, item=item)

if __name__ == '__main__':
    goods_dao = GoodsClient('127.0.0.1', 27017, "test", "test")

    url = 'http://www.360buy.com/product/342079.html'
    name = "moto手机"
    cat = "手机"
    price = 1599

    goods_dao.put(url, name, cat, price)

    price = 1498
    goods_dao.put(url, name, cat, price)
