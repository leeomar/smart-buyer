#/bin/python
import time
from scrapy.xlib.pydispatch import dispatcher
from scrapy.exceptions import DontCloseSpider
from scrapy import signals
from scrapy import log
from scrapy.conf import settings

from price_trend.utils.url_util import get_uid
'''
seed file 

url\tcontent_group\tmax_idepth\tmax_xdepth\tcrawl_interval(seconnds)\tpriority


'''

class Seed(object):
    FIELD_NUM = 5

    def __init__(self, url, content_group, max_idepth, 
            max_xdepth, crawl_interval, priority):
        self.url = url 
        self.uid = get_uid(url)
        self.content_group = content_group 
        self.max_idepth = max_idepth 
        self.max_xdepth = max_xdepth
        self.crawl_interval = crawl_interval 
        self.priority = priority

    @classmethod
    def from_line(cls, line):
        fields = line.splite('\t')
        if len(fields) != Seed.FIELD_NUM:
            return  None

        return cls(fields[0], fields[1], fields[2], fields[3], fields[4])

class SeedAppend(object):

    def __init__(self):
        self.idle_spider = []
        self.request_list = []
        self.last_seed_time = {}
        self.last_update_time = None
        self.seeds_file = settings.get("SEED_FILE") 
        dispatcher.connect(self.spider_idle, signal=signals.spider_idle)

    def spider_idle(self):
        
        return DontCloseSpider

    def need_crawl(self, seed):
        cur_time = int(time.time())
        last_seed_time = self.last_seed_time.get(seed.uid, None)
        if last_seed_time is None \
            or cur_time - last_seed_time > seed.crawl_interval: 
            return True

        return False

    def load_seeds(self):
        f = open(self.seeds_file)
        while 1:
            line = f.readline()
            if not line:
                break

            item = Seed.from_line(line)
            if not item:
                continue

            if self.need_crawl(item):
                pass

    def make_request_from_seed(self, seed):
        pass

