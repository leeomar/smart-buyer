#/bin/python
import re
import string

def canonicalize_price(sprice):
    cprice = re.findall('([\d\.]+)', sprice)
    if len(cprice) == 0 or len(cprice) > 1:
        raise Exception("illegal price:%s" % sprice)

    return int(string.atof(cprice[0])*100)
