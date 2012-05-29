#/bin/python
from scrapy.xlib.pydispatch import dispatcher
from scrapy.exceptions import DontCloseSpider
from scrapy import signals
from scrapy import log
from scrapy.conf import settings
from scrapy.http import Request
from scrapy.project import crawler

import time
import sys
sys.path.append('gen-py.twisted')

from scheduler import Scheduler
from scheduler.ttypes import JobReport

from twisted.internet.defer import inlineCallbacks
from twisted.internet import reactor
from twisted.internet.protocol import ClientCreator

from thrift import Thrift
from thrift.transport import TTwisted
from thrift.protocol import TBinaryProtocol

class MasterClient(object):
    def __init__(self):
        self.is_requesting = False
        self.master_host = settings.get("MASTER_HOST")
        self.master_port = settings.get("MASTER_PORT")
        self.conn_timeout = settings.getint("DEFAULT_TIMEOUT", 30)
        self.conn_defer = self.connect()
        dispatcher.connect(self.handle_spider_idle, 
            signal=signals.spider_idle)

    def connect(self):
        d = ClientCreator(reactor,
                TTwisted.ThriftClientProtocol,
                Scheduler.Client,
                TBinaryProtocol.TBinaryProtocolFactory(),
            ).connectTCP(self.master_host, 
                self.master_port, self.conn_timeout)
        log.msg("prepare connect to Master[%s:%s]" % \
            (self.master_host, self.master_port))
        return d
        #d.addCallback(self.set_connect)
        #d.addErrback(self.close_conn)

    def set_connect(self, conn):
        self.conn = conn
        self.client = conn.client
        log.msg("connect to Master[%s:%s]" % \
            (self.master_host, self.master_port))
        return conn 

    def close_conn(self, obj):
        log.msg('connect error, fail connect to Master[%s:%s]' % \
            (self.master_host, self.master_port))
        self.conn = None
        self.client = None
        return obj

    #inlineCallbacks
    def get_seeds(self, conn):
        log.msg('get seeds')
        jobreport = JobReport()
        jobreport.spiderid = 'spider001'
        d = conn.client.get_seeds( \
            jobreport.spiderid, jobreport)
        d.addCallback(self.crawl_seeds)

    def crawl_seeds(self, pkg):
        print "crawl_seeds"
        for seed in pkg.seeds:
            req = self.make_request_from_seed(seed)
            #crawler.crawl(req, spider)
            print req

    def handle_spider_idle(self, spider):
        log.msg('%s idle' % spider.name)
        time.sleep(5)
        #self.conn_defer.addCallback(self.set_connect)
        self.conn_defer.addCallback(self.get_seeds)
        return DontCloseSpider

    def make_request_from_seed(self, seed):
        meta = {
                'cur_idepth' : seed.cur_idepth,
                'max_idepth' : seed.max_idepth,
                'cur_xdepth' : seed.cur_xdepth,
                'max_xdepth' : seed.max_xdepth,
                'priority' : seed.priority,
                'content_group' : seed.content_group,
                'pl_group' : seed.pl_group,
                'crawl_interval' : seed.crawl_interval,
            }
        request = Request(url=seed.url, meta = meta)
        return request
