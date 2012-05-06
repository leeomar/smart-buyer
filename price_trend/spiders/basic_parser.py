#/bin/python
# -*- coding: utf-8 -*-

import time
from scrapy import log
from scrapy.stats import stats
from scrapy.utils.url import urljoin_rfc
from scrapy.selector import XmlXPathSelector
from scrapy.utils.python import str_to_unicode
from scrapy.http.response.xml import XmlResponse
from scrapy.utils.python import str_to_unicode, unicode_to_str
from scrapy.http.response.text import TextResponse

from price_trend.utils.url_util import get_domain, get_uid
from urlparse import urlparse

class ReturnStatus:
    stop_it = 0
    move_on = 1

class BasicLinkInfo:
    
    def __init__(self, cur_idepth, max_idepth, \
            cur_xdepth, max_xdepth, content_group,\
            source, url):
        self.cur_idepth = cur_idepth
        self.max_idepth = max_idepth
        self.cur_xdepth = cur_xdepth
        self.max_xdepth = max_xdepth
        self.content_group = content_group
        self.source = source
        self.url = url
        self.uid = get_uid(url)
        self.domain = get_domain(url) 
        self.host = urlparse(self.url).hostname

    def __str__(self):
        return 'URL[%s], Host[%s], Int_Dep[%d/%d], Ext_Dep[%d/%d], Content_Group[%s], Source[%s]'\
            % (self.url, self.host, self.cur_idepth,
            self.max_idepth, self.cur_xdepth, self.max_xdepth, 
            self.content_group, self.source)
    
    @staticmethod
    def from_response(response):
        max_idepth = response.request.meta.get('max_idepth', 0)
        max_xdepth = response.request.meta.get('max_xdepth', 0)
        cur_idepth = response.request.meta.get('cur_idepth', 0) + 1
        cur_xdepth = response.request.meta.get('cur_xdepth', 0) + 1
        content_group = response.request.meta.get('content-group', None)
        source = response.request.meta.get('source', None)
        url = response.url
        return BasicLinkInfo(cur_idepth, max_idepth,\
            cur_xdepth, max_xdepth, content_group, source, url)

class BasicParser(object):

    def __init__(self):
        self.response = None
        self.basic_link_info = None
        self.spider = None 

    def init_context(self, response, basic_link_info, spider):
        self.response = response
        self.basic_link_info = basic_link_info
        self.spider = spider

    '''@Interface:
    '''
    def conditon_permit(self, response, basic_link_info, spider):
        if isinstance(response, TextResponse):
            return True
        else:
            return False

    '''@Interface: define default workflow
    '''
    def parse(self, response, basic_link_info, spider):
        if not self.conditon_permit(response, basic_link_info, spider):
            return  ReturnStatus.move_on
        
        self.log("use parser: %s" % type(self))
        self.init_context(response, basic_link_info, spider)
        self.save()
        self.expansion()

        if hasattr(self, 'cleanup'):
            self.cleanup()
        return ReturnStatus.stop_it
    
    def save(self):
        pass

    def expansion(self):
        if self.basic_link_info.max_idepth < self.basic_link_info.cur_idepth:
            return
        pass

    def log(self, msg, level=log.DEBUG):
        log.msg(msg, level=level, spider=self.spider)
