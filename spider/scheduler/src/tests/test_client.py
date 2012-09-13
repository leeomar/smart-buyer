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
    pkg = yield client.get_seeds(jobreport.spiderid, None, jobreport)

    for seed in pkg.seeds:
        wait = yield client.get_latency_time('spider001', seed.url)
        print '%s waits %s seconds' % (seed.url, wait)

    print pkg
    apkg = yield client.get_seeds(jobreport.spiderid, pkg, jobreport)
    print apkg

    reactor.stop()

def close(obj):
    print obj
    reactor.stop()

if __name__ == '__main__':
    try:
        import sys, getopt
        opts, args = getopt.getopt(sys.argv[1:], "h:p:", ["host=", "port="])
        host = '127.0.0.1' 
        port = 9091 
        for o, a in opts:
            if o in ("-h", "--host"):
                host  = a
            if o in ("-p", "--port"):
                port = int(a)
    except getopt.GetoptError:
        print "Usage: python client.py [-h|--host] [-p|--port]"
        sys.exit(1)

    print "connect scheduler[%s:%s]" % (host, port)
    d = ClientCreator(reactor,
        TTwisted.ThriftClientProtocol,
        Scheduler.Client,
        TBinaryProtocol.TBinaryProtocolFactory(),
        ).connectTCP(host, port, timeout=30)
    d.addCallback(lambda conn: conn.client)
    d.addCallback(main)
    d.addErrback(close)
    reactor.run()
