#/bin/python

from downloader.utils.unicode import stringPartQ2B

def extract_value(xpathnode, encoding='utf-8'):
    value = ''.join(xpathnode.extract())
    return stringPartQ2B(value).encode(encoding) 
