# Scrapy settings for price_trend project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

LOG_FILE = 'spider.log'
BOT_NAME = 'price_trend'
BOT_VERSION = '1.0'
SELECTORS_BACKEND = "lxml"

SPIDER_MODULES = ['price_trend.spiders']
NEWSPIDER_MODULE = 'price_trend.spiders'
DEFAULT_ITEM_CLASS = 'price_trend.dao.goods_dao.GoodsItem'
#USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)
USER_AGENT = 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0)'

DOWNLOADER_MIDDLEWARES = {
    'price_trend.middlewares.hostpolite.HostPoliteCtrlMiddleware' : 200,
    'scrapy.contrib.downloadermiddleware.redirect.RedirectMiddleware' : 100,
    'scrapy.contrib.downloadermiddleware.stats.DownloaderStats' : 300,
    'scrapy.contrib.downloadermiddleware.robotstxt.RobotsTxtMiddleware' : 500,
    'scrapy.contrib.downloadermiddleware.retry.RetryMiddleware' : 700,
}

EXTENSIONS = {
    'price_trend.seeder.AutoSeedAppend': 0,
    'scrapy.contrib.resolver.CachingResolver': 0
}

SPIDER_PARSERS = {
    "price_trend.spider.basic_parser.BasicParser",
}

#persistence layer group Mapping
PLG_MAPPING = {
    "360buy.com" : "360buy",
    "okbuy.com" : 'okbuy',
    "letao.com" : 'letao',
    "price_monitor" : 'real_time_price',
}
