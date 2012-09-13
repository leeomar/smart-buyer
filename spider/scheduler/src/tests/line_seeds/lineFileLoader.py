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

def parse_line(line):
    try:
        dic=json.loads(line)
        seed = Seed()
        seed.url = dic['url']
        seed.content_group = dic['content_group']
        seed.pl_group = dic.get('pl_group', seed.content_group)
        seed.max_idepth = dic.get('max_idepth', 0)
        seed.max_xdepth = dic.get('max_xdepth', 0)
        seed.priority = dic.get('priority', 0)
        seed.crawl_interval = dic.get('crawl_interval', 10)
        seed.seed_frequency = dic.get('seed_frequency', 0)
        return seed
    except Exception, e:
        print e
        raise
        return None

def parse_file(filename):
    f = open(filename)
    pkg = SeedsPackage()
    pkg.ID = 'FileSeedsLoader'
    pkg.seeds = []
    while 1:
        line = f.readline()
        #print line
        
        if not line:
            break

        if line.find("#")==0:
            print "ignore line[%s]" % line
            continue
        
        seed = parse_line(line)
        if seed:
            pkg.seeds.append(seed)
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
    reactor.run()

if __name__ == '__main__':
    main()
