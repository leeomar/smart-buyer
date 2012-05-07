#/bin/python
import time
import Queue
from scrapy.xlib.pydispatch import dispatcher
from scrapy.exceptions import DontCloseSpider
from scrapy import signals
from scrapy import log
from scrapy.conf import settings
from scrapy.http import Request
from scrapy.project import crawler
from price_trend.utils.url_util import get_uid
from scrapy.utils.reactor import CallLaterOnce

'''
seed file: 
url\tcontent_group\tmax_idepth\tmax_xdepth\tcrawl_interval(seconnds)\tpriority\tpl_group
'''

class Seed(object):
    FIELD_NUM = 6

    def __init__(self, url, content_group, max_idepth, 
            max_xdepth, crawl_interval, priority, pl_group):
        self.url = url 
        self.uid = get_uid(url)
        self.content_group = content_group 
        self.max_idepth = max_idepth 
        self.max_xdepth = max_xdepth
        self.crawl_interval = crawl_interval 
        self.priority = priority
        self.pl_group = pl_group #persistent layer group

    def __str__(self):
        return "Seed[url:%s, uid:%s, cg:%s, max_idepth:%s, \
            max_xdepth:%s, craw_interval:%s, priority:%s, plg: %s]" % \
            (self.url, self.uid, self.content_group, self.max_idepth, 
             self.max_xdepth, self.crawl_interval, self.priority,
             self.pl_group
            )

    @classmethod
    def from_line(cls, line):
        fields = line.splite('\t')
        if len(fields) != Seed.FIELD_NUM:
            log.msg("bad seed[%s], field num[%s], expect[%s]" %(line,
                len(fields), Seed.FIELD_NUM), level=log.ERROR)
            return  None

        return cls(fields[0], fields[1], fields[2], fields[3], 
            fields[4], fields[5])

#TODO add mutex
class RequestSlot(object):

    def __init__(self):
        self.pending_request_queue = Queue.PriorityQueue() 
        self.pending_uids_map = {}

    def put(self, request, priority=3):
        uid = request.meta['uid']
        if uid in self.pending_uids_map:
            return

        self.pending_request_queue.put((priority, request))
        self.pending_uids_map[request.meta['uid']] = 1
        
    def get(self, timeout=-1):
        priority, request = self.pending_request_queue.get(
            timeout=timeout)
        del self.pending_uids_map[request.meta['uid']]
        return request

    def empty(self):
        return self.pending_request_queue.empty()

class SeedAppend(object):
    DEFAULT_BATCH_SIZE = 5
    DEFAULT_QUEUE_TIMEOUT = 10
    DEFAULT_LOAD_SEED_INTERVAL = 10

    def __init__(self):
        self.idle_spider = []
        self.pending_requests = RequestSlot() 
        self.last_crawl_time = {}
        self.last_seed_time = 0 
        self.seeds_file = settings.get("SEED_FILE") 
        dispatcher.connect(self.handle_spider_idle, signal=signals.spider_idle)
        self.nextcall = CallLaterOnce(self.load_seeds)

    def handle_spider_idle(self, spider):
        #crawler.engine.crawl(request, self) 
        if self.pending_requests.empty():
            self.nextcall.schedule()
        else:
            num = 0
            while num < SeedAppend.DEFAULT_BATCH_SIZE \
                and self.pending_requests.empty() is False:
                #priority, request = self.pending_request_queue.get(
                #    timeout=SeedAppend.DEFAULT_QUEUE_TIMEOUT)
                request = self.pending_requests.get(
                    timeout=SeedAppend.DEFAULT_QUEUE_TIMEOUT)
                self.last_crawl_time[request.meta['uid']] = int(time.time())
                crawler.engine.crawl(request, spider)
                num += 1
        return DontCloseSpider

    def need_crawl(self, seed):
        cur_time = int(time.time())
        last_crawl_time = self.last_crawl_time.get(seed.uid, None)
        if last_crawl_time is None \
            or cur_time - last_crawl_time > seed.crawl_interval: 
            return True

        return False

    def load_seeds(self):
        left_time = SeedAppend.DEFAULT_LOAD_SEED_INTERVAL - \
            (int(time.time()) - self.last_seed_time) 
        if left_time > 0:
            self.nextcall.schedule(left_time)
    
        f = open(self.seeds_file)
        if f is None:
            log.msg('FATAL, fail open %s' % self.seeds_file, level=log.ERROR)
            return

        while 1:
            line = f.readline()
            if not line:
                break

            item = Seed.from_line(line)
            if not item:
                continue

            if self.need_crawl(item):
                #TODO: if url is aready in pending_request_queue, then no need to add again
                request = self.make_request_from_seed(item)
                #self.pending_request_queue.put((item.priority, request))
                self.pending_requests.put(request, item.priority)
                log.msg("load %s" % item, level=log.DEBUG)

        self.last_seed_time = int(time.time())
        self.nextcall.schedule(SeedAppend.DEFAULT_LOAD_SEED_INTERVAL)

    def make_request_from_seed(self, seed):
        meta = {
                'uid' : seed.uid,
                'cur_idepth' : 0,
                'max_idepth' : seed.max_idepth,
                'cur_xdepth' : 0,
                'max_xdepth' : seed.max_xdepth,
                'priority' : seed.priority,
                'content_group' : seed.content_group,
            }
        request = Request(url=seed.url, meta = meta)
        return request
