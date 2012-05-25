#!/usr/bin/env python

import sys
sys.path.append('../../gen-py.twisted')

from scheduler import Scheduler

from twisted.internet.defer import inlineCallbacks
from twisted.internet import reactor
from twisted.internet.protocol import ClientCreator

from thrift import Thrift
from thrift.transport import TTwisted
from thrift.protocol import TBinaryProtocol

def output(num):
    print num

@inlineCallbacks
def main(client):
    print 'client run'
    yield client.ping()

    result = yield client.get_latency_time('spider001', 'http://www.sina.cn')
    print result

    reactor.stop()

if __name__ == '__main__':
    d = ClientCreator(reactor,
        TTwisted.ThriftClientProtocol,
        Scheduler.Client,
        TBinaryProtocol.TBinaryProtocolFactory(),
        ).connectTCP("127.0.0.1", 9090)
    d.addCallback(lambda conn: conn.client)
    d.addCallback(main)
    reactor.run()
