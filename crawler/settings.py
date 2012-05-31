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
DEFAULT_ITEM_CLASS = 'crawler.dao.goods_dao.GoodsItem'
SPIDER_MANAGER_CLASS = 'crawler.extensions.spidermanager.MySpiderManager'
#USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)
USER_AGENT = 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0)'

DOWNLOADER_MIDDLEWARES = {
    'crawler.middlewares.hostpolite.HostPoliteCtrlMiddleware' : 200,
    'scrapy.contrib.downloadermiddleware.redirect.RedirectMiddleware' : 100,
    'scrapy.contrib.downloadermiddleware.stats.DownloaderStats' : 300,
    'scrapy.contrib.downloadermiddleware.robotstxt.RobotsTxtMiddleware' : 500,
    'scrapy.contrib.downloadermiddleware.retry.RetryMiddleware' : 700,
}

EXTENSIONS = {
    'crawler.extensions.masterclient.MasterClient': 0,
    'scrapy.contrib.resolver.CachingResolver': 20,
}

SPIDER_PARSERS = {
    "crawler.parsers.buy360.Buy360Parser" : 0,
}

#persistence layer group Mapping
PLG_MAPPING = {
    "360buy.com" : "360buy",
    "okbuy.com" : 'okbuy',
    "letao.com" : 'letao',
    "price_monitor" : 'intime_price',
}

MONGODB_HOST='127.0.0.1'
MONGODB_PORT=27017
MONGODB_DBNAME='price_trend'
DEFAULT_COLLECTION_NAME='default_collection'

MASTER_HOST='127.0.0.1'
MASTER_PORT=9090
DEFAULT_TIMEOUT=10
