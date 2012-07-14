# Scrapy settings for price_trend project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

LOG_FILE = 'spider.log'
BOT_NAME = 'crawler'
BOT_VERSION = '1.0'
SELECTORS_BACKEND = "lxml"

SPIDER_MODULES = ['crawler.spiders']
NEWSPIDER_MODULE = 'crawler.spiders'
#DEFAULT_ITEM_CLASS = 'crawler.dao.goods.GoodsItem'
#USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)
USER_AGENT = 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0)'

SPIDER_MANAGER_CLASS = 'crawler.extensions.spidermanager.MySpiderManager'
STATS_CLASS = 'scrapy.statscol.MemoryStatsCollector'
STATS_ENABLED = True
STATS_DUMP = False

DOWNLOADER_MIDDLEWARES = {
    'crawler.middlewares.hostpolite.HostPoliteCtrlMiddleware' : 100,
    'crawler.middlewares.js.JsMiddleware' : 150,

    'scrapy.contrib.downloadermiddleware.redirect.RedirectMiddleware' : 200,
    'scrapy.contrib.downloadermiddleware.stats.DownloaderStats' : 300,
    'scrapy.contrib.downloadermiddleware.robotstxt.RobotsTxtMiddleware' : 500,
    'scrapy.contrib.downloadermiddleware.retry.RetryMiddleware' : 700,
    'crawler.middlewares.bandwidth.BandwidthMiddleware' : 1000,
}

EXTENSIONS = {
    'crawler.extensions.masterclient.MasterClient': 0,
    'crawler.extensions.signalhandler.SignalHandler': 10,
    'crawler.extensions.report.StatesReport': 30,
    'scrapy.contrib.resolver.CachingResolver': 50,
}

SPIDER_PARSERS = {
    "crawler.parsers.buy360.Buy360Parser" : 0,
    "crawler.parsers.letao.LetaoParser" : 0,
    "crawler.parsers.okbuy.OkbuyParser" : 0,
}

#persistence layer group Mapping
PLG_MAPPING = {
    "buy360" : "buy360",
    "okbuy" : 'okbuy',
    "letao" : 'letao',
    "monitor" : 'intime',
}

MAIL_SERVER = {
    "host" : "",
    "user" : "",
    "pwd"  : "",
    "from" : "",
}

MONGODB = {
    'host' : '127.0.0.1',
    'port' : 27017,
    'db' : 'price',
    'default_collection': 'default',
}

REDIS = {
    'host' : '127.0.0.1',
    'port' : 6379,
    'db' : 0,
    'expire' :  60*60*24*7,
}

MASTER = {
    'host' : '127.0.0.1',
    'port' : 9090,
    'timeout' : 10,
}

TMP_FILE_DIR='/tmp'
ACCEPT_DISCOUNT = 0.7

JS_SITES = [
    'http://suning.com/',        
]
