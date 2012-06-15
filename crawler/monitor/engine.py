# -*- coding: utf-8 -*-
'''
user subscription rules will be stored in mongodb,
in the following format:
    {
        oid: ,
        url: ,
        uid: ,
        email: ,
        price: ,
        discount: ,
        xpath: ,
        frequency: ,
    }

    xpath:
    {
        oid: ,
        url: ,
        uid: ,
        xpath: ,
        frequency: ,
    }
'''
from crawler.utils.email import EmailClient
from crawler.dal.mymongo import MongoClient
from crawler.dal.item import GoodsItem
from crawler.utils.url import get_uid
from scrapy import log

class Rule(object):
    COLLECTION = 'rules'

    def __init__(self, dbsettings):
        self.mongo = MongoClient.from_settings(dbsettings).open()

    def get(self, uid, price, discount):
        if not price or not discount:
            raise Exception('price and discount cannot be both None')

        # { $or : [ { a : 1 } , { b : 2 } ] }
        rules = self.mongo.find(self.COLLECTION, 
            { '$or' : [
                {'uid': uid, 'price' : {'$lte': price}},
                {'uid': uid, 'discount': {'$lte': discount}}
            ]})

        emails = []
        for rule in rules:
            emails.appent(rule['email'])
        return emails


class PriceMonitorEngine(object):
    def __init__(self, dbsettings, mailsettings, discount):
        self.rule = Rule(dbsettings) 
        self.mail = EmailClient.from_settings(mailsettings) 
        self.accept_discount = discount
    
    @classmethod
    def from_settings(cls, settings):
        dbsettings = settings.get('MONGODB')
        mailsettings = settings.get('MAIL_SERVER')
        discount = settings.get('ACCEPT_DISCOUNT')
        return cls(dbsettings, mailsettings, discount)

    #action will be triggered by 80 percent sale
    def process(self, item):
        if not isinstance(item, GoodsItem):
            log.msg('expect a GoodsItem instance, got %s' % type(item))
            return

        if len(item.data) < 2:
            return

        #compare the latest and second latest price
        discount = float(item.data[-1][0])/item.data[-2][0]
        if discount > self.accept_discount:
            return

        price = item.data[-1][0]
        recipients = self.rule.get(get_uid(item.url), price, discount)
        subject = 'Big Promotion[$title]'
        content = "$title is now ￥%s, discount %s, %s" % (price, discount, item.url)
        self.mail.send(recipients, subject, content)
