#/bin/python
# -*- coding: utf-8 -*-

from crawler.dao.mongoclient import MongoClient
from crawler.utils.url_util import get_uid, get_domain
from crawler.dao.item import GoodsItem
import time
    
class GoodsDAO:

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
            self.dbclient.insert_field(uid, collection_name, 
                data=(price, crawl_time),)
            if price <= goods_item.get_bottom_price():
                self.dbclient.update_field(uid, collection_name, 
                   bottom_price=(price, crawl_time))
        elif not goods_item.duplicate_price_item(price, crawl_time):
            self.dbclient.insert(
                {   "url":url, 'uid': uid,  "name":name, 
                    "cat":cat, "data":[(price, crawl_time)], 
                    "bottom_price":(price, crawl_time), 
                    "domain=":domain
                 }, uid, collection_name)
        else:
            #TODO log here
            pass
       
        print goods_item 

if __name__ == '__main__':
    goods_dao = GoodsDAO('127.0.0.1', 27017, "test", "test")

    url = 'http://www.360buy.com/product/342079.html'
    name = "moto手机"
    cat = "手机"
    price = 1599

    goods_dao.put(url, name, cat, price)

    price = 1498
    goods_dao.put(url, name, cat, price)
