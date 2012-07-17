#/bin/python
# -*- coding: utf-8 -*-
from downloader.utils.time import is_same_day

class GoodsItem:
    MAX_PRICE_NUM = 90
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
        self.bottom_price=()
        self.domain=None

    def get_price(self, idx):
        return self.data[idx][0]

    def get_time(self, idx):
        return self.data[idx][1]

    def add_price(self, price, crawl_time):
        last = -1
        if len(self.data) == 0:
            self.data.append((price, crawl_time))
        elif not is_same_day(self.get_time(last), crawl_time):
            self.data.append((price, crawl_time))
        elif self.get_price(last) >  price:
            #only save the min price in one day
            self.data[-1] = (price, crawl_time)
        else:
            #get a higher price in one day
            return False
        
        #update bottom price
        if len(self.bottom_price) == 0 \
            or price < self.bottom_price[0]:
            self.bottom_price = (price, crawl_time)

        self.ensure_data_num()
        return True

    def ensure_data_num(self):
        if self.data and len(self.data) > self.MAX_PRICE_NUM:
            self.data = self.data[-self.MAX_PRICE_NUM:]
    
    '''
    def duplicate_price_item(self, price, crawl_time):
        last = -1
        if len(self.data) > 0 and \
            self.get_price(last) == price and \
            is_same_day(self.get_time(last), crawl_time):
            return True
        else:
            return False
    '''

    def get_bottom_price(self):
        return self.bottom_price[0]
