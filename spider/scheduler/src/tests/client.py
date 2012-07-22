#!/usr/bin/env python

import sys
sys.path.append('../protocol/gen-py.twisted')

from scheduler import Scheduler
from scheduler.ttypes import JobReport

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

    jobreport = JobReport()
    jobreport.spiderid = 'spider001'
    pkg = yield client.get_seeds(jobreport.spiderid, jobreport)
    print pkg

    for seed in pkg.seeds:
        wait = yield client.get_latency_time('spider001', seed.url)
        print '%s waits %s seconds' % (seed.url, wait)

    reactor.stop()

def close(obj):
    print obj
    reactor.stop()

if __name__ == '__main__':
    d = ClientCreator(reactor,
        TTwisted.ThriftClientProtocol,
        Scheduler.Client,
        TBinaryProtocol.TBinaryProtocolFactory(),
        ).connectTCP("127.0.0.1", 9090, timeout=30)
    d.addCallback(lambda conn: conn.client)
    d.addCallback(main)
    d.addErrback(close)
    reactor.run()
