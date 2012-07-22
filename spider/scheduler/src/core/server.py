#!/usr/bin/env python
import sys
sys.path.append('protocol/gen-py.twisted')

import time
from scheduler import Scheduler
#from scheduler.ttypes import Seed, SeedsPackage
#from scheduler.ttypes import JobReport, ServerError
#from scheduler.ttypes import RequestError

from zope.interface import implements
from thrift.transport import TTwisted
from thrift.protocol import TBinaryProtocol
#from thrift.server import TServer

from twisted.application import internet, service
from twisted.python.logfile import DailyLogFile
from twisted.python.log import ILogObserver, FileLogObserver
from twisted.python import log

from core.seeder import MemoryBasedSeedsService
from core.engine import AutoseedingEngine
from utils.struct_format import *
from conf import settings

class RequestHandler:
    implements(Scheduler.Iface)
    def __init__(self, seed_service):
        self.seed_service = seed_service
        self.autoseeding_engine = AutoseedingEngine(self.seed_service)
        log.msg('init RequestHandler')

    def ping(self):
        log.msg("ping received")
        print 'ping()'

    def do_register(self, spiderid):
        pass 

    def do_unregister(self, spiderid):
        pass

    def get_seeds(self, spiderid, report):
        log.msg("Request get_seeds from %s" % spiderid)
        seeds = self.seed_service.get_seeds(spiderid, report)
        pkg = SeedsPackage()
        pkg.ID = "pkg%s" % int(time.time()) 
        pkg.seeds = seeds
        log.msg('return SeedsPackage[%s] to %s, total %s seeds' % \
            (pkg.ID, spiderid, len(pkg.seeds)))
        return pkg

    def add_seeds(self, clientid, pkg):
        log.msg("Request add_seeds from %s, %s" %\
            (clientid, format_seedspackage(pkg)))
        self.seed_service.add_seeds(clientid, pkg)
        self.autoseeding_engine.add_package(pkg)
        log.msg("finish process add_seeds from %s" % clientid)
        return

    def get_latency_time(self, spiderid, url):
        log.msg('Request get_latency_time from %s, url:%s' % \
            (spiderid, url))
        wait = self.seed_service.get_latency_time(url)
        return wait 

def make_application():
    ssetings = settings.get('SERVER')
    port = ssetings['port']

    pkg_size = settings.getint("SEED_PKG_SIZE")
    seed_servie = MemoryBasedSeedsService(pkg_size)
    handler = RequestHandler(seed_servie)
    processor = Scheduler.Processor(handler)

    factory = TTwisted.ThriftServerFactory(processor,
        TBinaryProtocol.TBinaryProtocolFactory())
    tcp_service = internet.TCPServer(port, factory)

    application = service.Application(ssetings['name'])
    logfile = DailyLogFile(settings.get('LOG_FILE'), settings.get('LOG_DIR'))
    application.setComponent(ILogObserver, FileLogObserver(logfile).emit)

    multiService = service.MultiService()
    tcp_service.setServiceParent(multiService)
    multiService.setServiceParent(application)
    return application

application = make_application()
#server = reactor.listenTCP(9090,
#    TTwisted.ThriftServerFactory(processor,
#    pfactory), interface="127.0.0.1")
