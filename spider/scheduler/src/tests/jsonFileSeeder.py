#!/usr/bin/env python

import sys
sys.path.append('../protocol/gen-py.twisted')

from scheduler import Scheduler
from scheduler.ttypes import Seed, SeedsPackage

from twisted.internet.defer import inlineCallbacks
from twisted.internet import reactor
from twisted.internet.protocol import ClientCreator

from thrift import Thrift
from thrift.transport import TTwisted
from thrift.protocol import TBinaryProtocol
import json

def print_error(obj):
    print obj
    reactor.stop()

def parse_file(filename):
    print "parse %s" % filename
    f = open(filename)
    seeds_array = json.loads(f.read())
    if isinstance(seeds_array, dict):
        seeds_array = [seeds_array, ]

    pkg = SeedsPackage()
    pkg.ID = 'FileSeedsLoader'
    pkg.seeds = []
    for item in seeds_array: 
        try:
            seed = Seed()
            seed.url = item['url']
            seed.content_group = item['content_group']
            seed.pl_group = item.get('pl_group', seed.content_group)
            seed.max_idepth = item.get('max_idepth', 0)
            seed.max_xdepth = item.get('max_xdepth', 0)
            seed.priority = item.get('priority', 0)
            seed.crawl_interval = item.get('crawl_interval', 10)
            seed.seed_frequency = item.get('seed_frequency', 0)
            pkg.seeds.append(seed)
        except Exception, e:
            print "skip %s, Exception %s" % (item, e)
            continue
    print pkg
    return pkg

@inlineCallbacks
def call_add_seeds(client, seed_file):
    yield client.ping()

    spkg = parse_file(seed_file)
    print 'invoke add seeds'
    yield client.add_seeds('FileSeedsLoader', spkg)
    reactor.stop()

def main():
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

        if len(args) != 1:
            print 'expect seeds file name'
            sys.exit(2)

        seeds_file = args[0]
    except getopt.GetoptError:
        print "Usage: python loader.py [-h|--host] [-p|--port] seeds_file"
        sys.exit(2)

    print "connect scheduler[%s:%s]" % (host, port)
    d = ClientCreator(reactor,
        TTwisted.ThriftClientProtocol,
        Scheduler.Client,
        TBinaryProtocol.TBinaryProtocolFactory(),
        ).connectTCP(host, port)
    d.addCallback(lambda conn: conn.client)
    d.addCallback(call_add_seeds, seeds_file)
    d.addErrback(print_error)
    reactor.run()

if __name__ == '__main__':
    #parse_file(sys.argv[1])
    main()
