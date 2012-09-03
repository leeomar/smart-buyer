import os
import time
import fcntl
import subprocess
from cStringIO import StringIO

'''
CUR_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
PYPHANTOMJS_CMD = "phantomjs"
PYPHANTOMJS_CONFIG = "--config=%s/config.json" % CUR_DIRECTORY
PYPHANTOMJS_JS = "%s/load_page.js" % CUR_DIRECTORY
'''
def fread(fobj, noblock=False):
    if noblock:
        fd = fobj.fileno()
        fl = fcntl.fcntl(fd, fcntl.F_GETFL)
        fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)
        try:
            return fobj.read()
        except:
            return None 
    else:
        fobj.readlines()

class PyPhantomJs(object):
    def __init__(self, phantom_path):
        self.cmd = 'phantomjs' % phantom_path
        self.config = "--config=%s/config.json" % phantom_path
        self.js = "%s/load_page.js" % phantom_path

    def load_page(self, url, timeout=30, bufsize=1*1024*1024):
        process = subprocess.Popen(
            [self.cmd, self.config, self.js, url],
            bufsize=bufsize, stdout=subprocess.PIPE)
    
        start_time = time.time()
        buf = StringIO()
        istimeout = True 
        while time.time() - start_time <= timeout:
            tmp = fread(process.stdout, noblock=True)
            if tmp:
                buf.write(tmp)

            if process.poll() is None:
                time.sleep(0.01)
                continue
            else:
                istimeout = False 
                break
    
        if istimeout:
            buf.write('timeout')
            process.terminate()

        content = buf.getvalue()
        buf.close()
        rc = 1 if istimeout else process.wait()
        return rc, url, content 

'''
block read
content = process.stdout.readlines()
process.stdout.close()
process.terminate()
return process.wait(), content
'''
if __name__ == '__main__':
    import sys
    if len(sys.argv) != 2:
        print 'Usage: pyphantomjs url'
        sys.exit(2)

    curdir = "%s/phantomjs_1_6" % os.path.dirname(os.path.realpath(__file__))
    phantom = PyPhantomJs(curdir)
    print phantom.load_page(sys.argv[1])

'''
from twisted.internet import defer
from twisted.internet import threads
from twisted.internet import reactor
def defer_load_page(url, timeout=10, bufsize=1*1024*1024):
    d = threads.deferToThread(load_page, url, timeout, bufsize)
    return d 

def printdata(data):
    print data

def stopTwisted(param):
    reactor.stop()

def test_defer():
    defers = []
    with open(sys.argv[1]) as f:
        while 1:
            url = f.readline()
            if not url:
                break
            d = defer_load_page(url) 
            d.addBoth(printdata)
            defers.append(d)
    
    dl = defer.DeferredList(defers)
    dl.addBoth(stopTwisted)
    reactor.run()
'''
