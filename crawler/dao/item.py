#/bin/python
# -*- coding: utf-8 -*-

from crawler.utils.datetimeutil import is_same_day

class GoodsItem:
    
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
    def __init__(self):
        self.oid=None
        self.uid=None
        self.url=None
        self.name=None
        self.cat=None
        self.data={}
        self.bottom_price={}
        self.domain=None

    def get_price(self, idx):
        return self.data[idx][0]

    def get_time(self, idx):
        return self.data[idx][1]

    def duplicate_price_item(self, price, crawl_time):
        last = -1
        if len(self.data) > 0 and \
            self.get_price(last) == price and \
            is_same_day(self.get_time(last), crawl_time):
            return True
        else:
            return False

    def get_bottom_price(self):
        return self.bottom_price[0]
