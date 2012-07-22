import os
import time
import fcntl
import subprocess
from cStringIO import StringIO

PYPHANTOMJS_ROOT = "%s/phantomjs_1_6" % os.path.dirname(os.path.realpath(__file__))
PYPHANTOMJS_CMD = "phantomjs"
#PYPHANTOMJS_CMD = "%s/bin/phantomjs" % PYPHANTOMJS_ROOT
PYPHANTOMJS_CONFIG = "--config=%s/config.json"  % PYPHANTOMJS_ROOT 
PYPHANTOMJS_JS = "%s/load_page.js" % PYPHANTOMJS_ROOT

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

def load_page(url, timeout=10, bufsize=1*1024*1024):
    process = subprocess.Popen(
        [PYPHANTOMJS_CMD, PYPHANTOMJS_CONFIG, PYPHANTOMJS_JS, url],
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

if __name__ == '__main__':
    #print load_page('http://www.baidu.com')
    #print load_page('awww.abaidu.com')
    import sys
    if len(sys.argv) != 2:
        print 'Usage: pyphantomjs url_file'
        sys.exit(2)
    print sys.argv
    d = defer_load_page(sys.argv[1]) 
    d.addBoth(printdata)
    d.addBoth(stopTwisted)
    reactor.run()

    '''
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
