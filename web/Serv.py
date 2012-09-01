#!/bin/python
# -*- coding: utf-8 -*-
import tornado.ioloop
import tornado.web
import tornado.autoreload
import tornado.escape
import string
import traceback 
from datetime import datetime

from conf import settings
from url import get_uid, get_domain
from mymongo import MongoClient

def json(s):
    return tornado.escape.json_encode(s)

def timestamp2strtime(timestamp, fmt='"%Y-%m-%d"'):
    return datetime.fromtimestamp(timestamp).strftime(fmt)

class WatchHandler(tornado.web.RequestHandler):
    #def post(self, url, xpath, acceptable_price, acceptable_discount, email, notify_frequency, watch_period):
    def post(self):
        '''
        @parameters:
            url: 需要监控的商品URL地址
            xpath: 价格标签的scrapy语法的xpath信息
            acceptable_price:　可接受的商品价格
            acceptable_discount: 可接受的价格折扣, acceptable_price和acceptable_discount必须任选其一
            email: 接收邮件提醒的用户email地址
            notify_frequency: 提醒频率, 以秒为单位,　例如:notify_frequency＝3600, 即最多一小时一次
            watch_period: 监控有效期,　以秒为单位,　最长一个月. 例如:　watch_period＝7*3600, 监控一星期
        '''
        try:
            print self.request
            url = self.get_argument('url')
            xpath = self.get_argument('xpath')
            acceptable_price = self.get_argument('acceptable_price')
            acceptable_discount = self.get_argument('acceptable_discount')
            email = self.get_argument('email')
            notify_frequency = self.get_argument('notify_frequency')
            watch_period = self.get_argument('watch_period')
            print url
            print xpath
            print acceptable_price
            print acceptable_discount
            print email
            print notify_frequency
            print watch_period
        except Exception, e:
            print e
            self.write(json({'status': '404', 'msg': 'invalide parameter'}))
        self.write(json({'status' : '200'}))
        
class PriceHandler(tornado.web.RequestHandler):
    def get(self):
        url = self.get_argument('url', None)
        if url is None:
            self.write(json({'status' : 400}))
        ''' 
        url = url_normalize(url)
        if url is None:
            self.write(json({}))
        '''
        try:

            domain = get_domain(url)
            table = domain_table_mapping.get(domain)
            print "[%s], domain:%s, table:%s" % (url, domain, table)

            item = mongo.find_one(get_uid(url), table)
            print item
            if item is None:
                self.write(json({'status' : 401, 'msg' : 'sorry for no data'}))
                return

            timeline = [timestamp2strtime(data[1]) for data in item['data']]
            dataline = [float(data[0])/100 for data in item['data']]

            self.write(
                json(
                    {
                     'status' : 200, 
                     'prod_name' : item['name'],
                     'bottom_price' : [float(item['bottom_price'][0])/100,
                         timestamp2strtime(item['bottom_price'][1]) ],
                     'timeline' : timeline, 
                     'series' :
                        [{'name': item['domain'], 'data': dataline}] 
                    }
                  )
                )
        except BaseException, err:
            print err
            traceback.print_exc()
            self.write(json({'status' : 400}))

app = tornado.web.Application([
    (r"/smartbuyer/price/", PriceHandler),
    (r"/smartbuyer/watch/", WatchHandler),
    ])
mongo = MongoClient.from_settings(settings.get('MONGODB'))
mongo.open()
domain_table_mapping = settings.get('DOMAIN_TABLE_MAPPING')

if __name__ == "__main__":
    app.listen(10001)
    loop = tornado.ioloop.IOLoop.instance()
    tornado.autoreload.start(loop)
    loop.start()
