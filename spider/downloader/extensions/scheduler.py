#/bin/python
from scrapy.xlib.pydispatch import dispatcher
from scrapy.exceptions import DontCloseSpider
from scrapy import signals
from scrapy import log
from scrapy.conf import settings
from scrapy.http import Request
from scrapy.project import crawler

from downloader.scheduler import Scheduler
from downloader.scheduler.ttypes import JobReport

from twisted.internet import reactor
from twisted.internet.protocol import ClientCreator
from twisted.internet import defer

from thrift import Thrift
from thrift.transport import TTwisted
from thrift.protocol import TBinaryProtocol

class SchedulerClient(object):
    def __init__(self):
        self.is_requesting = False

        msettings = settings.get('SCHEDULER_ADDR')
        self.host = msettings['host'] 
        self.port = msettings['port']
        self.timeout = msettings.get('timeout', 30)

        self.last_pkg = None
        self.conn_defer = self.connect()
        self.conn = None
        dispatcher.connect(self.handle_spider_idle, 
            signal=signals.spider_idle)

    def connect(self):
        d = ClientCreator(reactor,
                TTwisted.ThriftClientProtocol,
                Scheduler.Client,
                TBinaryProtocol.TBinaryProtocolFactory(),
            ).connectTCP(self.host, 
                self.port, self.timeout)
        d.addCallback(self.set_connect)
        d.addErrback(self.close_conn)
        log.msg("try connect to Scheduler[%s:%s]" % \
            (self.host, self.port))
        return d

    def set_connect(self, conn):
        self.conn = conn
        self.conn_defer = None
        log.msg("connect to Scheduler[%s:%s]" % \
            (self.host, self.port), level=log.INFO)

    def close_conn(self, failure):
        self.conn = None
        self.conn_defer = None
        log.msg('fail connect to Scheduler[%s:%s]' % \
            (self.host, self.port), level=log.ERROR)

    @defer.inlineCallbacks
    def get_seeds(self, spider):
        log.msg("%s send seeds request" % spider.name)
        jobreport = JobReport()
        jobreport.spiderid = spider.name 

        pkg = yield self.conn.client.get_seeds( \
            jobreport.spiderid, self.last_pkg, jobreport)
        for seed in pkg.seeds:
            req = self.make_request_from_seed(seed)
            crawler.engine.crawl(req, spider)
            log.msg("crawl %s" % req.url)

        self.last_pkg = pkg

    def handle_spider_idle(self, spider):
        #log.msg('%s idle' % spider.name)
        if self.conn:
            self.get_seeds(spider)
        raise DontCloseSpider

    def make_request_from_seed(self, seed):
        meta = {
                'cur_idepth' : seed.cur_idepth,
                'max_idepth' : seed.max_idepth,
                'cur_xdepth' : seed.cur_xdepth,
                'max_xdepth' : seed.max_xdepth,
                'priority' : seed.priority,
                'pl_group' : seed.pl_group,
                'content_group' : seed.content_group,
                'crawl_interval' : seed.crawl_interval,
            }
        request = Request(url=seed.url, meta = meta)
        return request
