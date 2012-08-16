import tornado.ioloop
import tornado.web
import tornado.autoreload
import tornado.escape
import string
import traceback 
from datetime import datetime

from conf import settings
from url import get_uid, get_domain
from mymongo import MongoClient

def json(s):
    return tornado.escape.json_encode(s)

def timestamp2strtime(timestamp, fmt='"%Y-%m-%d"'):
    return datetime.fromtimestamp(timestamp).strftime(fmt)

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
        url = self.get_argument('url', None)
        if url is None:
            self.write(json({'status' : 400}))
            return
        ''' 
        url = url_normalize(url)
        if url is None:
            self.write(json({}))
        '''
        try:

            domain = get_domain(url)
            table = domain_table_mapping.get(domain)
            print "[%s], domain:%s, table:%s" % (url, domain, table)

            item = dbclient.find_one(get_uid(url), table)
            print item


            timeline = [timestamp2strtime(data[1]) for data in item['data']]
            dataline = [float(data[0])/100 for data in item['data']]

            self.write(
                json(
                    {
                     'status' : 200, 
                     'timeline' : timeline, 
                     'series' :
                        [{'name': item['domain'], 'data': dataline}] 
                    }
                  )
                )
        except BaseException, err:
            print err
            traceback.print_exc()
            self.write(json({'status' : 400}))

app = tornado.web.Application([
    (r"/smartbuyer/price", PriceTrendHandler),
    (r"/", MainHandler),
    ])
dbclient = MongoClient.from_settings(settings.get('MONGODB'))
dbclient.open()
domain_table_mapping = settings.get('DOMAIN_TABLE_MAPPING')

if __name__ == "__main__":
    app.listen(10001)
    loop = tornado.ioloop.IOLoop.instance()
    tornado.autoreload.start(loop)
    loop.start()
