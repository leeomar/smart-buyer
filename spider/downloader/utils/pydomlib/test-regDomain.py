#
# Calculate the effective registered domain of a fully qualified domain name.
#
# <@LICENSE>
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to you under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at:
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# </@LICENSE>
#
# Florian Sager, 2009-01-11, sager@agitos.de
# 
# Python translation:
# TAGAMI Yukihiro, 2010-09-06, tagami.yukihiro@gmail.com
#

import sys

import regDomain
import effectiveTLDs

argv = sys.argv[1:]
argc = len(argv)

if argc == 0: 
	print "test-regDomain.py <(fully-qualified-domain-name )+>\n"
	sys.exit(1)

# strip subdomains from every signing domain
for i in range(argc):

	registeredDomain = regDomain.getRegisteredDomain(argv[i], effectiveTLDs.tldTree)

	if registeredDomain == None:
		print "error: %s" % argv[i]
	else:
		print "%s" % registeredDomain

sys.exit(0);
