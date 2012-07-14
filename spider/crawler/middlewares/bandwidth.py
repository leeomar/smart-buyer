#/bin/python

from scrapy.stats import stats
from scrapy import log

class BandwidthMiddleware(object):

    def process_response(self, request, response, spider):
        stats.inc_value('crawled_url_num', spider=spider)
        stats.inc_value('crawled_page_size', 
            count=len(response.body), spider=spider)
        #log.msg('download page:%s, size:%s, content-length:%s'\
        #    %(response.url, len(response.body),
        #    response.headers.get('Content-Length')))
        return response
