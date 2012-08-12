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

#getRegisteredDomain(signingdomain)
#
#Remove subdomains from a signing domain to get the registered domain.
#
#dkim-reputation.org blocks signing domains on the level of registered domains
#to rate senders who use e.g. a.spamdomain.tld, b.spamdomain.tld, ... under
#the most common identifier - the registered domain - finally.

def getRegisteredDomain(signingDomain, treeNode_ref):

	signingDomainParts = signingDomain.split(".")

	result = findRegisteredDomain(treeNode_ref, signingDomainParts)

	if result == None:
		# this is an invalid domain name
		return None

	# assure there is at least 1 TLD in the stripped signing domain
	if result.find('.') == -1:
		cnt = len(signingDomainParts)
		if cnt <= 1:
			return None
		return signingDomainParts[-2] + "." + signingDomainParts[-1]
	else:
		return result

# recursive helper method
def findRegisteredDomain(treeNode_ref, remainingSigningDomainParts):

	if len(remainingSigningDomainParts) > 0:
		sub = remainingSigningDomainParts.pop()
	else:
		sub = None

	if not sub:
		sub = None

	result = None

	if '!' in treeNode_ref:
		return '#'
	elif sub in treeNode_ref:
		result = findRegisteredDomain(treeNode_ref[sub], remainingSigningDomainParts)
	elif '*' in treeNode_ref:
		result = findRegisteredDomain(treeNode_ref['*'], remainingSigningDomainParts)
	else: 
		return sub

	if result == '#':
		return sub
	elif result != None and len(result) > 0:
		return result + "." + sub
	return None

