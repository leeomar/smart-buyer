#!/usr/bin/env python
import time
from twisted.python import log
from utils.url import get_domain

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
    default_crawl_interval = 1

    def __init__(self, name, priority=0, 
            last_crawl_time=None, crawl_interval=None,
            total_url_num=0, crawled_url_num=0,
            pending_url_num=0, running_url_num=0):
        self.name = name 
        self.priority = priority 
        self.last_crawl_time = last_crawl_time 
        
        if crawl_interval:
            self.crawl_interval = crawl_interval 
        else:
            self.crawl_interval = HostInfo.default_crawl_interval
        
        self.total_url_num = total_url_num 
        self.crawled_url_num = crawled_url_num
        self.pending_url_num = pending_url_num
        self.running_url_num = running_url_num
        #self.pending_urls = Queue.PriorityQueue() 
    
    @classmethod
    def from_seed(cls, seed):
        name = get_domain(seed.url)
        priority = seed.priority
        crawl_interval = seed.crawl_interval
        return cls(name=name, priority=priority, 
            crawl_interval=crawl_interval, total_url_num=1)

    def inc_total_url_num(self):
        self.total_url_num += 1

    def __str__(self):
        return "Host[name:%s, priority:%s, crawl_interval:%s,\
    last_crawl_time:%s, total_url_num:%s, crawled_url_num:%s,\
    pending_url_num:%s, running_url_num:%s]" % (self.name, self.priority,
            self.crawl_interval, self.last_crawl_time, self.total_url_num,
            self.crawled_url_num, self.pending_url_num, self.running_url_num)

class GlobalInfo(object):

    def __init__(self):
        self.start_time = time.time()
        self.spiders = {} 
        self.hosts = {}

    def do_register(self, spiderid):
        if spiderid in self.spiders:
            return
        else:
            spider_info = SpiderInfo(spiderid)
            self.spiders[spiderid] = spider_info 

    def do_unregister(self, spiderid):
        if spiderid in self.spiders:
            self.spiders[spiderid].update()
        else:
            pass

    def update_spider_report(self, report, isbusy):
        self.do_register(report.spiderid)
        self.spiders[report.spiderid].update(report, isbusy)

    def add_seed(self, seed):
        domain = get_domain(seed.url)
        hostinfo = self.hosts.get(domain)
        if hostinfo:
            hostinfo.total_url_num += 1
        else:
            self.hosts[domain] = HostInfo.from_seed(seed)
            log.msg('add new host:%s' % domain)
