#/bin/python

from .baseparser import BaseParser
from scrapy.selector import HtmlXPathSelector

from crawler.utils.selector import extract_value
from crawler.utils.goods import canonicalize_price

#http://www.letao.com/shoe-a-a-a-a-a-a-a-a-p1-n
class LetaoParser(BaseParser):
    ALLOW_CGS =['letao', ]
    BASE_URL = "http://www.letao.com"

    def process(self):
        item_num = 0
        hxs = HtmlXPathSelector(self.response)
        prolist = hxs.select('//div[@id="prodlist"]/li')
        for item in prolist:
            url = "%s%s" % (self.BASE_URL ,
                    extract_value(item.select('a/@href')))
            sprice = extract_value(
                item.select('p[@class="pimg"]/span[@class="pinfo"]/i[@class="ltprice"]/text()')
                )
            price = canonicalize_price(sprice)
            name = extract_value(
                item.select('p[@class="pimg"]/span[@class="pname"]/a/text()')
                )
            self.save(url, name, (), price)
            item_num += 1

        self.next_page(hxs)
        return item_num

    def next_page(self, hxs):
        urls = \
            hxs.select('//p[@id="pageupper"]/a[@class="next"]/@href').extract()
        if urls:
            request = self.make_request_from_response(
                    "%s%s" % (self.BASE_URL, urls[0]),
                )
            self.crawl(request)
            self.log('next page:%s' % request.url)
