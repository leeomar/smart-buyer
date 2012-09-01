# Scrapy settings for price_trend project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

LOG_FILE = 'spider.log'
BOT_NAME = 'downloader'
BOT_VERSION = '1.0'
SELECTORS_BACKEND = "lxml"

SPIDER_MODULES = ['downloader.spiders']
NEWSPIDER_MODULE = 'downloader.spiders'
USER_AGENT = 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0)'

SPIDER_MANAGER_CLASS = 'downloader.extensions.spidermanager.MySpiderManager'
STATS_CLASS = 'scrapy.statscol.MemoryStatsCollector'
STATS_ENABLED = True
STATS_DUMP = False

DOWNLOADER_MIDDLEWARES = {
    'downloader.middlewares.hostpolite.HostPoliteCtrlMiddleware' : 100,
    'downloader.middlewares.js.JsMiddleware' : 150,

    'scrapy.contrib.downloadermiddleware.cookies.CookiesMiddleware' : 180,
    'scrapy.contrib.downloadermiddleware.redirect.RedirectMiddleware' : 200,
    'scrapy.contrib.downloadermiddleware.stats.DownloaderStats' : 300,
    'scrapy.contrib.downloadermiddleware.robotstxt.RobotsTxtMiddleware' : 500,
    'scrapy.contrib.downloadermiddleware.retry.RetryMiddleware' : 700,

    'downloader.middlewares.bandwidth.BandwidthMiddleware' : 1000,
}

EXTENSIONS = {
    'downloader.extensions.scheduler.SchedulerClient': 0,
    'downloader.extensions.signalhandler.SignalHandler': 10,
    'downloader.extensions.report.StatesReport': 30,
    #'scrapy.contrib.resolver.CachingResolver': 50,
}

SPIDER_PARSERS = {
    "downloader.parsers.buy360.Buy360Parser" : 0,
    "downloader.parsers.letao.LetaoParser" : 0,
    "downloader.parsers.okbuy.OkbuyParser" : 0,
    "downloader.parsers.suning.SuningParser" : 0,
    "downloader.parsers.tmall.TmallParser" : 0,
}

#persistence layer group Mapping
PLG_MAPPING = {
    "buy360" : "buy360",
    "okbuy" : 'okbuy',
    "letao" : 'letao',
    "suning" : 'suning',
    "monitor" : 'monitor',
    "tmall" : "kele",
}

MAIL_SERVER = {
    "host" : "smartbuyer.me@gmail.com",
    "user" : "smartbuyer.me",
    "pwd"  : "smart1234",
    "from" : "smartbuyer.me@gmail.com",
}

MONGODB = {
    'host' : '127.0.0.1',
    'port' : 27017,
    'db' : 'smartbuyer',
    'default_collection': 'default',
}

REDIS = {
    'host' : '127.0.0.1',
    'port' : 6379,
    'db' : 0,
    'default_expire' :  60*60*24*7,
}

SCHEDULER_ADDR = {
    'host' : '127.0.0.1',
    'port' : 9091,
    'timeout' : 10,
}

UPYUN = {
        'bucket' : 'kele-img',
        'username' : 'kele-admin',
        'password' : 'omar1984',
}

TMP_FILE_DIR='/tmp'
ACCEPT_DISCOUNT = 0.7

JS_PATTERNS = [
    'http://www.suning.com/emall/',        
]
PHANTOMJS_PATH = '/Users/lijian/Applications/phantomjs-1.6.1-macosx-static' 

ENABLE_SOLR=True
SOLR="http://localhost:8983/solr"
