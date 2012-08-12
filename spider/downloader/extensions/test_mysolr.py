#!/bin/python
# -*- coding: utf-8 -*- 
import solr
from scrapy import log
#from mysolr import MySolr
#from downloader.dal.record import ProductRecord

def decode(text, encoding='utf-8'):
    return text
    #return text.decode(encoding)

class MySolr(object):

    def __init__(self, url):
        self.solr_url = url

    def add(self, record):
        #if not isinstance(record, (ProductRecord, dict)):
        #    log.msg("expect Product Record, got %s") % type(record)
        #    return

        # create a connection to a solr server
        s = solr.SolrConnection(self.solr_url)
        '''
            prod_name=u"天伦天 男士 春季新款 户外运动防水鞋 1075",
            prod_cat=[u"运动健康", u"户外鞋服", u"户外鞋袜"],
            prod_price=49900,
            prod_domain='360buy.com',
            #prod_ts="",
            #prod_valid="",
        '''
        # add a document to the index
        s.add(id=record['uid'], 
                prod_uid = record['uid'],
                prod_url = record['url'], 
                prod_name = decode(record['name']),
                prod_cat = [ decode(item) for item in record['cat'] ],
                prod_price = record['data'][-1][0],
                prod_domain = record['domain']
            )
        s.commit()
        log.msg('add %s, %s to solr' % (record['url'], record['name']))

    def query(self, text):
        # create a connection to a solr server
        s = solr.SolrConnection(self.solr_url)
        # do a search
        response = s.query(text)
        for hit in response.results:
            print hit['prod_name']

if __name__ == '__main__':
    record = { #"_id" : ObjectId("5024971bd04df0715500077a"), 
                "domain" : "360buy.com", 
                "uid" : "3e37d45bbf1d93ae", 
                "bottom_price" : [ 49900, 1344575259 ], 
                "url" : "http://www.360buy.com/product/1005442199.html", 
                "cat" : ["运动健康", "户外鞋服", "户外鞋袜" ], 
                "data" : [ [ 49900, 1344575259 ] ], 
                "name" : "天伦天 男士 春季新款户外运动防水鞋 1075"
            }
    obj = MySolr('http://localhost:8983/solr')
    obj.add(record)
