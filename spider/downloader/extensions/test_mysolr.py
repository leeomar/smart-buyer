#!/bin/python
# -*- coding: utf-8 -*- 
import solr
from scrapy import log
from mysolr import MySolr




if __name__ == '__main__':
    record = { #"_id" : ObjectId("5024971bd04df0715500077a"), 
                "domain" : "360buy.com", 
                "uid" : "3e37d45bbf1d93ae", 
                "bottom_price" : [ 49900, 1344575259 ], 
                "url" : "http://www.360buy.com/product/1005442199.html", 
                "cat" : [u"运动健康", u"户外鞋服", u"户外鞋袜" ], 
                "data" : [ [ 49900, 1344575259 ] ], 
                "name" : u"天伦天 男士 春季新款户外运动防水鞋 1075"
            }

    record = {'domain': u'360buy.com', 'uid': 'aa7a7030fa68697', 'bottom_price': (9800, 1347072708), 'url': u'http://www.360buy.com/product/509428.html', 'cat': ['\xe8\xbd\xa6\xe8\xbd\xbd\xe7\x94\xb5\xe6\xba\x90'], 'data': [(9800, 1347072708)], 'name': '\xe5\x8d\xa1\xe7\x99\xbb\xe4\xbb\x95\xef\xbc\x88CAPDASE\xef\xbc\x892.1A\xe8\xb6\x85\xe7\x9f\xadMini USB \xe4\xb8\x87\xe8\x83\xbd\xe8\xbd\xa6\xe5\x85\x85\xef\xbc\x88CACB-PPT1\xef\xbc\x89\xe7\x81\xb0\xe8\x89\xb2 \xe9\x80\x9a\xe7\x94\xa8\xe4\xba\x8e\xe8\x8b\xb9\xe6\x9e\x9ciPad iPhone iPod\xe7\xb3\xbb\xe5\x88\x97'}

    obj = MySolr('http://localhost:8983/solr')
    obj.add(record)
