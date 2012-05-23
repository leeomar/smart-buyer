#!/usr/bin/env python

import sys
sys.path.append('../gen-py.twisted')

from iservice import SeedsService
from iservice.ttypes import *

from twisted.internet.defer import inlineCallbacks
from twisted.internet import reactor
from twisted.internet.protocol import ClientCreator

from thrift import Thrift
from thrift.transport import TTwisted
from thrift.protocol import TBinaryProtocol

@inlineCallbacks
def main(client):
    print 'client run'
    result = yield client.get_latency_time('spider001', 'http://www.sina.cn')
    print result

    reactor.stop()

if __name__ == '__main__':
    d = ClientCreator(reactor,
        TTwisted.ThriftClientProtocol,
        SeedsService.Client,
        TBinaryProtocol.TBinaryProtocolFactory(),
        ).connectTCP('127.0.0.1', 9090)
    d.addCallback(lambda conn: conn.client)
    d.addCallback(main)
    reactor.run()
