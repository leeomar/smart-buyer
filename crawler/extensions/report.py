#/bin/python

from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
from scrapy.stats import stats
from scrapy import log

class StatesReport(object):

    def __init__(self):
        dispatcher.connect(self.print_report,
                signal=signals.stats_spider_closing)
        #scrapy.signals.stats_spider_opened(spider)

    def print_report(self, spider, reason):
        format_report = '\n'.join([
                "spider[%s] crawl report:" % spider.name,
                self.get_value('crawled_url_num', spider),
                self.get_value('crawled_page_size', spider),
            ])
        log.msg(format_report, level=log.INFO)

    def get_value(self, key, spider):
        return "%s: %s" %(key, stats.get_value(key, spider=spider))
