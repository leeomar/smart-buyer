#/bin/python

import os
import re
from scrapy import log
from .goods import canonicalize_price

def gocr(imagefile):
    s = os.popen('gocr %s' % imagefile).read()
    ss = re.sub('o', '0', s)
    log.msg('gocr %s, get [%s]' % (imagefile, ss))

    price = canonicalize_price(ss)
    log.msg('canonicalize_price, get [%s]' % price)
    return price
