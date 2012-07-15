import tornado.ioloop
import tornado.web
import tornado.autoreload
import tornado.escape
import string
from datetime import datetime

from mongo import *
from common import *

def json(s):
    return tornado.escape.json_encode(s)

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        '''
        http://localhost/  --> {arg: "NoUser"}
        http://localhost/?arg=username  --> {arg: "username"}
        '''
        arg = self.get_argument('arg', 'NoUser')
        self.write(json({'arg': arg}))
        
class PriceTrendHandler(tornado.web.RequestHandler):
    def get(self):
        t1 = datetime.now()
        url = self.get_argument('url', None)
        
        if url is None:
            self.write(json({'status' : 400}))
        ''' 
        url = url_normalize(url)
        if url is None:
            self.write(json({}))
        '''
        try:
            print "[%s]" % url
            print md5sum(url)
            re = CPriceTrendDao.query(md5sum(url))
            print re
            #timeline = [item['datetime'].strftime("%Y-%m-%d %H:%M:%S") for item in re['data']]
            timeline = [item['datetime'].strftime("%Y-%m-%d") for item in re['data']]
            dataline = [string.atof(item['price'])/100 for item in re['data']]

            t2 = datetime.now()
            print t2 - t1
            self.write(json({'status' : 200, 'timeline' : timeline, 'series' : [{'name': re['shop'], 'data': dataline}] }))
        except BaseException, err:
            print err
            self.write(json({'status' : 400}))

app = tornado.web.Application([
    (r"/price_trend", PriceTrendHandler),
    (r"/", MainHandler),
    ])

if __name__ == "__main__":
    app.listen(10001)
    loop = tornado.ioloop.IOLoop.instance()
    tornado.autoreload.start(loop)
    loop.start()
