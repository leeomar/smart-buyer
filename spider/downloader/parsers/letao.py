#/bin/python

from .baseparser import BaseParser
from scrapy.selector import HtmlXPathSelector

from downloader.utils.selector import extract_value
from downloader.utils.product import canonicalize_price

#http://www.letao.com/shoe-a-a-a-a-a-a-a-a-p1-n
class LetaoParser(BaseParser):
    ALLOW_CGS =['letao', ]

    def process(self):
        item_num = 0
        hxs = HtmlXPathSelector(self.response)
        prolist = hxs.select('//div[@id="prodlist"]/li')
        for item in prolist:
            prod_url = extract_value(item.select('a/@href'))
            sprice = extract_value(
                item.select('p[@class="pimg"]/span[@class="pinfo"]/i[@class="ltprice"]/text()')
                )
            price = canonicalize_price(sprice)
            prod_name = extract_value(
                item.select('p[@class="pimg"]/span[@class="pname"]/a/text()')
                )
            self.save(prod_url, prod_name, (), price)
            item_num += 1

        self.crawl_next_page()
        return item_num

    def next_page(self,):
        hxs = HtmlXPathSelector(self.response)
        urls = \
            hxs.select('//p[@id="pageupper"]/a[@class="next"]/@href').extract()
        if urls:
            return urls[0]
        else:
            return None
