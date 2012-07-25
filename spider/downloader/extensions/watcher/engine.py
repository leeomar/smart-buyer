# -*- coding: utf-8 -*-
'''
user subscription rules will be stored in mongodb,
in the following format:
    watch-rules:
    {
        oid: ,
        uid: ,
        url: ,
        email: ,
        price: ,
        discount: ,
        xpath: ,
        frequency: ,
    }

    watch-xpath:
    {
        oid: ,
        uid: ,
        url: ,
        xpath: ,
        frequency: ,
    }
    support frequency: 1min, 15min, 1h, 12h, 1day
'''
from downloader.utils.mail import EmailClient
from downloader.clients.mymongo import MongoClient
from downloader.dal.record import ProductRecord
from downloader.utils.url import get_uid
from scrapy import log

class Rule(object):
    COLLECTION = 'watch-rules'
    def __init__(self, dbsettings):
        self.mongo = MongoClient.from_settings(dbsettings)
        self.mongo.open()

    def get(self, uid, price, discount):
        if not price or not discount:
            raise Exception('price and discount cannot be both None')

        # { $or : [ { a : 1 } , { b : 2 } ] }
        rules = self.mongo.find(
                { '$or' : [
                    {'uid': uid, 'price' : {'$lte': price}},
                    {'uid': uid, 'discount': {'$lte': discount}}
                ]}, 
                self.COLLECTION
            )

        emails = []
        for rule in rules:
            emails.appent(rule['email'])
        return emails

class PriceWatcherEngine(object):
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
    def process(self, record):
        if not isinstance(record, (ProductRecord, dict)):
            log.msg('expect ProductRecord or dict, got %s' % type(record))
            return

        his_prices = record['data']
        discount = 100
        if his_prices and len(his_prices) >= 2:
            #compare the latest and second latest price
            discount = float(his_prices[-1][0])/his_prices[-2][0]
            if discount > self.accept_discount:
                return

        price = his_prices[-1][0]
        recipients = self.rule.get(get_uid(record['url']), price, discount)
        if recipients and len(recipients) > 0:
            subject = 'Big Promotion[$title]'
            content = "$title is now ￥%s, discount %s, %s" % (price, discount, record['url'])
            self.mail.send(recipients, subject, content)
