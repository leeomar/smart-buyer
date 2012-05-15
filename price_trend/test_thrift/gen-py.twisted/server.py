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

#from shared.ttypes import SharedStruct

from zope.interface import implements
from twisted.internet import reactor

from thrift.transport import TTwisted
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer

class UserStorageHandler:
    implements(UserStorage.Iface)  

    def store(user):
        pass
    
    def retrieve(uid):
        user = UserProfile()
        user.uid = 1
        user.name ='jack style'
        user.blurb = 'hi'
        return user


if __name__ == '__main__':
    handler = UserStorageHandler()
    processor = UserStorage.Processor(handler)
    pfactory = TBinaryProtocol.TBinaryProtocolFactory()
    server = reactor.listenTCP(9090,
                TTwisted.ThriftServerFactory(processor,
                pfactory), interface="127.0.0.1")
    reactor.run()
