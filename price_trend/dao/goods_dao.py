#/bin/python
# -*- coding: utf-8 -*-

from price_trend.dao.mongo_client import MongoClient
from price_trend.utils.url_util import get_uid, get_domain
import time

class GoodsItem:
    
    def __init__(self):
        self.uid=None
        self.url=None
        self.name=None
        self.cat=None
        self.data={}
        self.bottom_price={}
        self.domain=None

class GoodsDAO:

    '''
        goods storage format:
        {
            '_id' : 4fa6122145880006ef000000,
            'uid' : ,
            'url' : ,
            'name': ,
            'cat' : ,
            'domain': ,
            
            'data' : [
                (price, crawl_time), 
            ]

            'bottom_price' : (price, crawl_time)
        }
    '''
    def __init__(self, host, port, dbname, collection_name):
        self.dbclient = MongoClient().connect(
                host, port, dbname, collection_name)

    def add(self, url, name, cat, price):
        uid = get_uid(url)
        domain = get_domain(url)
        crawl_time = int(time.time()) 
        record = self.dbclient.find_one(pk=uid)
        if record:
            self.dbclient.insert_field(pk=uid,  
                data=(price, crawl_time),)
            if price <= record['bottom_price']:
                self.dbclient.update_field(pk=uid, 
                   bottom_price=(price, crawl_time))
        else:
            self.dbclient.insert(
                {   "url":url, "name":name, 
                    "cat":cat, "data":[(price, crawl_time)], 
                    "bottom_price":(price, crawl_time), 
                    "domain=":domain
                 }, pk=uid)
       
        print record 

if __name__ == '__main__':
    goods_dao = GoodsDAO('127.0.0.1', 27017, "test", "test")

    url = 'http://www.360buy.com/product/342079.html'
    name = "moto手机"
    cat = "手机"
    price = 1599

    goods_dao.add(url, name, cat, price)

    price = 1498
    goods_dao.add(url, name, cat, price)


