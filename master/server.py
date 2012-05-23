#!/usr/bin/env python

import sys
sys.path.append('../gen-py.twisted')

from iservice import SeedsService
from iservice import RegistService
from iservice.ttypes import *

from zope.interface import implements
from twisted.internet import reactor

from thrift.transport import TTwisted
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer

class SeedsServiceHandler:
    implements(SeedsService.Iface)

    def __init__(self):
        print 'init handle'

    '''
    def spider_register(spiderid):
        pass

    def spider_unregister(spiderid):
        pass
    '''

    def get_seeds(spiderid, report):
        pkg = SeedsPackage('pkg001', [])
        return pkg 

    def add_seeds(spiderid, pkg):
        print 'add seeds'
        return

    def get_latency_time(spiderid, url):
        print 'got request'
        print spiderid, url
        return 1

if __name__ == '__main__':
        handler = SeedsServiceHandler()
        processor = SeedsService.Processor(handler)
        pfactory = TBinaryProtocol.TBinaryProtocolFactory()
        server = reactor.listenTCP(9090, 
            TTwisted.ThriftServerFactory(processor,
            pfactory), interface='127.0.0.1')

        reactor.run()
