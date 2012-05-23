#!/usr/bin/env python

#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements. See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership. The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License. You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied. See the License for the
# specific language governing permissions and limitations
# under the License.
#

import sys
sys.path.append('../gen-py.twisted')

from a import UserStorage
from a.ttypes import *

from twisted.internet.defer import inlineCallbacks
from twisted.internet import reactor
from twisted.internet.protocol import ClientCreator

from thrift import Thrift
from thrift.transport import TTwisted
from thrift.protocol import TBinaryProtocol

@inlineCallbacks
def main(client):
    print 'got client'
    user = yield client.retrieve(11)
    print user

    reactor.stop()

if __name__ == '__main__':
    d = ClientCreator(reactor,
                      TTwisted.ThriftClientProtocol,
                      UserStorage.Client,
                      TBinaryProtocol.TBinaryProtocolFactory(),
                      ).connectTCP("127.0.0.1", 9095)
    d.addCallback(lambda conn: conn.client)
    d.addCallback(main)

    reactor.run()
