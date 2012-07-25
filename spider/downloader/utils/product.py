#/bin/python
import re
import string

def canonicalize_price(sprice):
    print sprice
    cprice = re.findall('([\d\.]+)', sprice)
    print cprice
    if len(cprice) == 0 or len(cprice) > 1:
        raise Exception("illegal price:%s" % sprice)

    return int(string.atof(cprice[0])*100)
