#!/bin/python
# -*- coding: utf-8 -*- 
from scrapy import log
from downloader.dal.record import ProductRecord
import solr

def decode(text, encoding='utf-8'):
    return text.decode(encoding)

class MySolr(object):

    def __init__(self, url):
        self.solr_url = url

    def add(self, record):
        if not isinstance(record, (ProductRecord, dict)):
            log.msg("expect Product Record, got %s") % type(record)
            return

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
        s.add( id = record['uid'], 
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
