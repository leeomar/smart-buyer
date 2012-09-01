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

    def add_doc(self, doc):
        # create a connection to a solr server
        s = solr.SolrConnection(self.solr_url)
        # add a document to the index
        s.add(doc) 
        s.commit()
        log.msg('add %s to solr' % doc) 

    def add(self, record):
        if not isinstance(record, (ProductRecord, dict)):
            log.msg("expect Product Record, got %s") % type(record)
            return

        doc = { id : record['uid'], 
                prod_uid : record['uid'],
                prod_url : record['url'], 
                prod_name : decode(record['name']),
                prod_cat : [ decode(item) for item in record['cat'] ],
                prod_price : record['data'][-1][0],
                prod_domain : record['domain']
            }
        self.add_doc(doc)

    def query(self, text):
        # create a connection to a solr server
        s = solr.SolrConnection(self.solr_url)
        # do a search
        response = s.query(text)
        for hit in response.results:
            print hit['prod_name']
