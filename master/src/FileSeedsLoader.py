#!/usr/bin/env python

import sys
sys.path.append('../../gen-py.twisted')

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
        print line
        
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
def main(client):
    yield client.ping()

    spkg = parse_file('test_seeds.file')
    print 'invoke add seeds'
    yield client.add_seeds('FileSeedsLoader', spkg)
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
