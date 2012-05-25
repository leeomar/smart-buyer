#!/usr/bin/env python
import sys
sys.path.append('../../gen-py.twisted')
sys.path.append('../../common')

from scheduler import Scheduler
from scheduler.ttypes import Seed, SeedsPackage
from scheduler.ttypes import JobReport, ServerError
from scheduler.ttypes import RequestError

from zope.interface import implements
from twisted.internet import reactor

from thrift.transport import TTwisted
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer

from struct_format import *

from log import log

class SchedulerHandler:
    implements(Scheduler.Iface)
    def __init__(self):
        log.info('init SchedulerHandler')

    def ping(self):
        log.debug("ping received")
        print 'ping()'

    def do_register(self, spiderid):
        pass 

    def do_unregister(self, spiderid):
        pass

    def get_seeds(self, spiderid, report):
        pass

    def add_seeds(self, clientid, pkg):
        log.debug("got seed package[%s] from %s" % (clientid, pkg.ID))
        print format_seedspackage(pkg)
        print 'add seeds'
        return

    def get_latency_time(self, spiderid, url):
        print spiderid, url
        return 0

if __name__ == '__main__':
    handler = SchedulerHandler()
    processor = Scheduler.Processor(handler)
    pfactory = TBinaryProtocol.TBinaryProtocolFactory()
    server = reactor.listenTCP(9090,
        TTwisted.ThriftServerFactory(processor,
        pfactory), interface="127.0.0.1")
    reactor.run()
