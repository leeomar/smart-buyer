#/bin/python
import time
import Queue
from utils import get_domain
from reactor import CallLaterOnce

'''
seed file: 
{
    host1:list<seed>,
    host2:list<seed>
}
'''
class Host(object):
    default_crawl_interval = 1

    def __init__(self, host,):
        self.name = None
        self.priority = 0
        self.last_crawl_time = None
        self.crawl_interval = Host.default_crawl_interval
        
        self.total_url_num = 0
        self.crawled_url_num = 0
        self.pending_url_num = 0
        self.running_url_num = 0
        #self.pending_urls = Queue.PriorityQueue() 

class SeedsService:
    SEED_PKG_SIZE = 5
    
    def __init__(self):
        self.pending_seeds = []
        self.candidate_seeds = []
        self.host_info = {}

        self.load_seeds_call= CallLaterOnce(self._load_seeds)
        self.load_seeds_call.schedule()

    def get_seeds(self, spiderid):
        num = 0
        while num < self.SEED_PKG_SIZE \
            and len(self.pending_seeds) > 0:
            num += 1
            yield self.pending_seeds[0]
            del self.pending_seeds[0]

    def add_seeds(self, clientid, pkg):
        for seed in pkg:
            self.candidate_seeds.append(seed)

    def get_latency_time(self, url):
        domain = get_domain(url) 
        hostinfo = self.host_info.get(domain, None)
        left_time = time.time() - hostinfo.last_crawl_time - \
            hostinfo.crawl_interval

        if left_time > 0:
            hostinfo.last_crawl_time = time.time()
            return 0 
        else:
            return -left_time

    def _caculate_url_priority(self, seed):
        domain = get_domain(seed.url)
        priority = self.host_info.get(domain, 0) 
        url_num = self.hostinfo_in_queue.get(domain, 0) 
        import math
        return int(1000*(priority + 1/(1+math.log(1+url_num))))

    def _load_seeds(self, force=False):
        if force or len(self.candidate_seeds) > 100:
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
