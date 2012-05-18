#/bin/python
import time
import Queue
from price_trend.utils.url_util import get_uid
from scrapy.utils.reactor import CallLaterOnce

'''
seed file: 
url\tcontent_group\tmax_idepth\tmax_xdepth\tcrawl_interval(seconnds)\tpriority\tpl_group

{
    host1:list<seed>,
    host2:list<seed>
}

runing
pending

use URL_DOWNLOAD_SIG, update last crawl time
'''

class GlobalInfo(object):
    
    def __init__(self):
        pass

class Host(object):
    default_crawl_interval

    def __init__(self, host,):
        self.host = None
        self.priority = 0
        self.last_crawl_time = None
        
        self.total_url_num = 0
        self.crawled_url_num = 0
        self.pending_url_num = 0
        self.running_url_num = 0
        
        self.pending_urls = Queue.PriorityQueue() 
        self.crawl_interval = Host.default_crawl_interval

class SpiderInfo(object):

    def __init__(self):
        self.busy = False
        self.crawled_url_num = 0

'''
appending_seeds = []
'''
class SeedsServiceImpl:
    SEED_PKG_SIZE = 5
    
    def __init__(self):
        self.pending_seeds = []
        self.host_info = {}
        self.candidate_seeds = []

        self.load_seeds_call= CallLaterOnce(self._load_seeds)
        self.load_seeds_call.schedule()

    def get_seeds(spiderid):
        num = 0
        while num < self.SEED_PKG_SIZE \
            and len(self.pending_seeds) > 0:
            num += 1
            yeild self.pending_seeds[0]
            del self.pending_seeds[0]

    #add seeds to candidate seeds list
    def add_seeds(pkg):
        for seed in pkg:
            self.candidate_seeds.append(seed)

    def get_latency_time(url):
        domain = get_domain(url) 
        hostinfo = self.host_info.get(domain, None)
        left_time = time.time() - hostinfo.last_crawl_time - \
            hostinfo.crawl_interval:

        if left_time > 0:
            hostinfo.last_crawl_time = time.time()
            return 0 
        else:
            return -left_time

    def _caculate_url_priority(seed):
        domain = get_domain(seed.url)
        priority = self.host_info.get(domain, 0) 
        url_num = self.hostinfo_in_queue.get(domain, 0) 
        import math
        return int(1000*(priority + 1/(1+math.log(1+url_num))))

    def has_appending_url():
        return len(self.appending_seeds) > 0 \
            or len(self.candidate_seeds) > 0

    def _load_seeds(force=False):
        if force or len(self.candidate_seeds) > 100:
            import Queue
            pq = Queue.PriorityQueue()
            self.hostinfo_in_queue = {}
            for i in range(0, len(self.candidate_seeds)):
                seed = self.candidate_seeds[i]
                priority = self._caculate_url_priority(seed)
                pq.put((priority, seed))

                domain = get_domain(seed.url)
                self.hostinfo_in_queue[domain] = \
                    self.hostinfo_in_queue.get(domain, 0) + 1
                del self.candidate_seeds[i]

            while pq.empty() is False:
                (priority, seed) = pq.pop()
                self.pending_seeds.append(seed)
            pq = None
            self.hostinfo_in_queue = None
        else:
            self.load_seeds_call.schedule(5)
            
