#/bin/python

import os
import re
from scrapy import log
from .goods import canonicalize_price

def gocr(imagefile):
    s = os.popen('gocr %s' % imagefile).read()
    ss = re.sub('o', '0', s)
    price = canonicalize_price(ss)

    #sprice = ''.join(re.findall('(\d+)', ss))
    #price = int(string.atof(sprice))
    log.msg('gocr %s, get [%s]' % (imagefile, price))
    return price
