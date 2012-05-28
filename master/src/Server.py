#!/usr/bin/env python
import sys
sys.path.append('../../gen-py.twisted')
sys.path.append('../../common')

import time
from scheduler import Scheduler
from scheduler.ttypes import Seed, SeedsPackage
from scheduler.ttypes import JobReport, ServerError
from scheduler.ttypes import RequestError

from zope.interface import implements
from twisted.internet import reactor

from thrift.transport import TTwisted
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer

from SeedsService import MemoryBasedSeedsService
from CycleSeederEngine import CycleSeederEngine

from struct_format import *
from log import log

class SchedulerHandler:
    implements(Scheduler.Iface)
    def __init__(self, seed_service):
        self.seed_service = seed_service
        self.cycle_seed_engine = CycleSeederEngine(self.seed_service)
        log.info('init SchedulerHandler')

    def ping(self):
        log.debug("ping received")
        print 'ping()'

    def do_register(self, spiderid):
        pass 

    def do_unregister(self, spiderid):
        pass

    def get_seeds(self, spiderid, report):
        log.debug("Request get_seeds from %s" % spiderid)
        seeds = self.seed_service.get_seeds(spiderid, report)
        pkg = SeedsPackage()
        pkg.ID = "pkg%s" % int(time.time()) 
        pkg.seeds = seeds
        log.debug('return SeedsPackage[%s] to %s, total %s seeds' % \
            (pkg.ID, spiderid, len(pkg.seeds)))
        return pkg

    def add_seeds(self, clientid, pkg):
        log.debug("Request add_seeds from %s, %s" %\
            (clientid, format_seedspackage(pkg)))
        self.seed_service.add_seeds(clientid, pkg)
        self.cycle_seed_engine.add_package(pkg)
        return

    def get_latency_time(self, spiderid, url):
        log.debug('Request get_latency_time from %s, url:%s' % \
            (spiderid, url))
        wait = self.seed_service.get_latency_time(url)
        return wait 

if __name__ == '__main__':
    seed_servie = MemoryBasedSeedsService()

    handler = SchedulerHandler(seed_servie)
    processor = Scheduler.Processor(handler)
    pfactory = TBinaryProtocol.TBinaryProtocolFactory()
    server = reactor.listenTCP(9090,
        TTwisted.ThriftServerFactory(processor,
        pfactory), interface="127.0.0.1")
    log.info('server starts')
    reactor.run()
