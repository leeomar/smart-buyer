#/bin/python
# -*- coding: utf-8 -*-

from scrapy.utils.signal import send_catch_log
from scrapy import log

from crawler import signals
from crawler.utils.url import get_uid, get_domain
from .mongoclient import MongoClient
from .item import GoodsItem
import time
    
class GoodsClient:

    def __init__(self, host, port, dbname, collection_name):
        self.dbclient = MongoClient().connect(
                host, port, dbname, collection_name)

    def get(self, url, collection_name=None):
        uid = get_uid(url)
        dbrecord = self.dbclient.find_one(uid, collection_name)
        if dbrecord:
            goods_item = GoodsItem()
            goods_item.oid = str(dbrecord['_id'])
            goods_item.url = dbrecord['url']
            goods_item.uid = dbrecord['uid']
            goods_item.name = dbrecord['name']
            goods_item.cat = dbrecord['cat']
            goods_item.data = dbrecord['data']
            goods_item.bottom_price = dbrecord['bottom_price']
            goods_item.domain = dbrecord['domain']
            return goods_item
        else:
            return None
    
    def put(self, url, name, cat, price, collection_name=None):
        uid = get_uid(url)
        domain = get_domain(url)
        crawl_time = int(time.time()) 
        goods_item = self.get(url, collection_name)
        if goods_item:
            if goods_item.add_price(price, crawl_time):
                self.dbclient.update_field(uid, collection_name, 
                    data=goods_item.data,
                    bottom_price=goods_item.bottom_price)
            else:
                log.msg('duplicate price')
        else: 
            self.dbclient.insert(
                {   "url":url, 'uid': uid,  "name":name, 
                    "cat":cat, "data":[(price, crawl_time)], 
                    "bottom_price":(price, crawl_time), 
                    "domain":domain
                 }, uid, collection_name)

        send_catch_log(signal=signals.item_saved,
            url=url, price=price, name=name, cat=cat)

if __name__ == '__main__':
    goods_dao = GoodsClient('127.0.0.1', 27017, "test", "test")

    url = 'http://www.360buy.com/product/342079.html'
    name = "moto手机"
    cat = "手机"
    price = 1599

    goods_dao.put(url, name, cat, price)

    price = 1498
    goods_dao.put(url, name, cat, price)
