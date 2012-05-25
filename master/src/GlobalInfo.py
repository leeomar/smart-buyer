#!/usr/bin/env python

import time
#from scheduler.ttypes import JobReport

class SpiderInfo(object):
    def __init__(self, spiderid):
        self.spiderid = spiderid
        self.register_time = time.time()
        self.last_update_time = self.register_time

        self.isbusy = False
        self.total_work_time = 0
        self.total_idle_time = 0

        self.crawled_url_num = 0
        self.crawled_page_size = 0
        self.fail_url_num = 0

    def update(self, jobreport=None, isbusy=False):
        self.isbusy = isbusy
        self.last_update_time = time.time()
        if jobreport:
            self.total_work_time += jobreport.work_time
            self.total_idle_time += jobreport.idle_time
            self.crawled_url_num += jobreport.crawled_url_num
            self.fail_url_num += jobreport.fail_url_num
            self.crawled_page_size += jobreport.crawled_page_size

    def __str__(self):
        return "{spiderid:%s, regsiter_time:%s, \
                last_update_time:%s, isbusy:%s, \
                total_work_time:%s, total_idle_time:%s, \
                crawled_url_num:%s, crawled_page_size:%s, \
                fail_url_num:%s}" % (self.spiderid, 
                self.regsiter_time, self.isbusy, 
                self.total_work_time, self.total_idle_time,
                self.crawled_url_num, self.crawled_page_size,
                self.fail_url_num)

class HostInfo(object):
    pass

class GlobalInfo(object):

    def __init__(self):
        self.start_time = time.time()
        self.registed_spiders = {} 

    def do_register(self, spiderid):
        if spiderid in self.registed_spiders:
            return
        else:
            spider_info = SpiderInfo(spiderid)
            self.registed_spiders[spiderid] = spider_info 


    def do_unregister(self, spiderid):
        if spiderid in self.registed_spiders:
            self.registed_spiders[spiderid].update()
        else:
            pass
