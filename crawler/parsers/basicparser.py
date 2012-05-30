#/bin/python
# -*- coding: utf-8 -*-

from scrapy.http.response.text import TextResponse
from crawler.logobj import LogableObject
from crawler.utils.url_util import get_domain, get_uid
from urlparse import urlparse

class ReturnStatus(object):
    stop_it = 0
    move_on = 1

class BasicLinkInfo(object):
    
    def __init__(self, cur_idepth, max_idepth, \
            cur_xdepth, max_xdepth, content_group, \
            pl_group, source, url):
        self.cur_idepth = cur_idepth
        self.max_idepth = max_idepth
        self.cur_xdepth = cur_xdepth
        self.max_xdepth = max_xdepth
        self.content_group = content_group
        self.pl_group = pl_group
        self.source = source
        self.url = url
        self.uid = get_uid(url)
        self.domain = get_domain(url) 
        self.host = urlparse(self.url).hostname

    def __str__(self):
        return 'URL[%s], Host[%s], Int_Dep[%d/%d], Ext_Dep[%d/%d],\
            Content_Group[%s], Pl_Group[%s], Source[%s]'\
            % (self.url, self.host, self.cur_idepth,
            self.max_idepth, self.cur_xdepth, self.max_xdepth, 
            self.content_group, self.pl_group, self.source)
    
    @staticmethod
    def from_response(response):
        max_idepth = response.request.meta.get('max_idepth', 0)
        max_xdepth = response.request.meta.get('max_xdepth', 0)
        cur_idepth = response.request.meta.get('cur_idepth', 0) + 1
        cur_xdepth = response.request.meta.get('cur_xdepth', 0) + 1
        content_group = response.request.meta.get('content-group', None)
        pl_group = response.request.meta.get('pl_group', None)
        source = response.request.meta.get('source', None)
        url = response.url
        return BasicLinkInfo(cur_idepth, max_idepth,\
            cur_xdepth, max_xdepth, content_group, pl_group, source, url)

class BasicParser(LogableObject):
    def __init__(self, plg_mapping):
        self.response = None
        self.basic_link_info = None
        self.spider = None 
        self.plg_mapping = plg_mapping
    
    @classmethod
    def from_settings(cls, settings):
        plg_mapping = settings.get("PLG_MAPPING")
        return cls(plg_mapping)

    def init_context(self, response, basic_link_info, spider):
        self.response = response
        self.basic_link_info = basic_link_info#BasicLinkInfo.from_response(response) 
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
        self.process()

        return ReturnStatus.stop_it

    def process(self):
        pass
    
    def get_collection_name(self):
        return self.plg_mapping.get(self.basic_link_info.pl_group)
