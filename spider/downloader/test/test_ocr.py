#!/bin/python

import sys
sys.path.append('../../')
from downloader.utils.ocr import gocr

if __name__ == '__main__':
    import sys
    if len(sys.argv) == 1:
        print "Usage: python test_ocr.py image_file"
        exit(1)

    price = gocr(sys.argv[1])
    print "gocr %s"
