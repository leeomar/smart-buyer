#/bin/python

import urllib2
import os
import re
import string
from .url import get_uid
from scrapy import log

DEFAULT_PATH='/tmp'
def gocr(url, tmpdir=None):
    if tmpdir is None:
        tmpdir = DEFAULT_PATH
    data = urllib2.urlopen(url).read()
    tmp_file = "%s/%s.tmp.png" % (tmpdir, get_uid(url))
    f = file(tmp_file, "wb")
    f.write(data)
    f.close()

    s = os.popen('gocr %s' % tmp_file).read()
    ss = re.sub('o', '0', s)
    sprice = ''.join(re.findall('(\d+)', ss))
    log.msg('gocr %s, get [%s]' % (url, sprice))
    price = int(string.atof(sprice))
    return price
