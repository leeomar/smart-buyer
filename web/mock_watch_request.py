#!/bin/python

import urllib
import urllib2

url = 'http://127.0.0.1:10001/smartbuyer/watch/'
values = {
    'url' : 'http://www.yougou.com/c_qX/p_99832581.shtml',
    'xpath' : '//div[contains(@id, "JDS_")]',
    'acceptable_price' : 120,
    'acceptable_discount' : 4,
    'email' : 'smartbuyer.me@gmail.com',
    'notify_frequency' : 3600,
    'watch_period' : 86400,
}

data = urllib.urlencode(values)
req = urllib2.Request(url, data)
response = urllib2.urlopen(req)
the_page = response.read()
