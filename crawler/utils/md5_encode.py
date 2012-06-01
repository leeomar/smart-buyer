#/bin/python
# -*- coding: utf-8 -*- 
import hashlib
import re
from claw.utils.unicodeutil import  stringQ2B

def md5_encode(param):
    m = hashlib.md5(param)
    m.digest()
    return m.hexdigest()

title_format=re.compile(':| ')
def normalize_title(orig_str, encode=None):
    #unicode
    if encode:
        orig_str = orig_str.decode(encode)
    orig_str = stringQ2B(orig_str)
    return title_format.sub('', orig_str).encode('utf-8')

if __name__=="__main__":
    ustring=u'中国 人名ａ高频：Ａ１２３４５６７８９０'
    print ustring
    nstring = normalize_title(ustring)
    print nstring
    print md5_encode(nstring)
