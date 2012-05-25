#/bin/python
from logging.handlers import RotatingFileHandler
import time
import os
import codecs

class DailyRotatingFileHandler(RotatingFileHandler):
    def __init__(self , filename , mode='a' , maxBytes=0, backupCount=0, encoding=None):
        self.current = time.strftime("%Y%m%d" , time.localtime(time.time()))
        self.path = os.path.dirname(filename)
        self.filename = os.path.basename(filename)
        newdir = os.path.join(self.path , self.current)
        if not os.access(newdir , os.X_OK):
            os.mkdir(newdir)
        newfile = os.path.join(newdir , self.filename)
        RotatingFileHandler.__init__(self, newfile , mode, maxBytes , backupCount , encoding)

    def doRollover(self):
        #print "doRollover , current=%s , filename=%s"%(self.current , self.baseFilename)
        self.stream.close()
        self.current = time.strftime("%Y%m%d" , time.localtime(time.time()))

        #newdir = os.path.join(self.path , repr(self.current))
        newdir = os.path.join(self.path , self.current)
        if not os.access(newdir , os.X_OK):
            os.mkdir(newdir)
        self.baseFilename = os.path.join(newdir , self.filename)

        if self.encoding:
            self.stream = codecs.open(self.baseFilename, 'w', self.encoding)
        else:
            self.stream = open(self.baseFilename, 'w')

    def shouldRollover(self, record):
        if RotatingFileHandler.shouldRollover(self , record):
            RotatingFileHandler.doRollover(self)

        t = time.strftime("%Y%m%d" , time.localtime(time.time()))
        if (cmp(self.current , t) < 0) :
            return 1

        return 0
