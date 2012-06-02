#/bin/python

from .baseparser import BaseParser
from scrapy.selector import HtmlXPathSelector

from crawler.utils.selector import extract_value
from crawler.utils.goods import canonicalize_price

#http://www.okbuy.com/product/search?category=clothes 
#http://www.okbuy.com/product/search?category=child_shoes
#http://www.okbuy.com/product/search?category=bags

#http://www.okbuy.com/product/search
#http://www.okbuy.com/product/ajax_find_listprice/16970593,16978450
#http://www.okbuy.com/product/detail/16970593.html?ref=l
#http://www.okbuy.com/product/search?&per_page=100#listheader
class OkbuyParser(BaseParser):
    ALLOW_CGS =['okbuy', ]
    BASE_URL = "http://www.okbuy.com/product/detail/"

    def process(self):
        item_num = 0
        hxs = HtmlXPathSelector(self.response)
        goods = hxs.select('//div[@class="floorConn"]/div[@class="goodsList"]/ul/li')
        gname_dict = {}
        gid_list = []
        for item in goods:
            name = extract_value(item.select('.//p[@class="productName"]/@title'))
            #url =  extract_value(item.select('div[@class="txt"]/a/@href'))
            gid = extract_value(item.select('.//span[@name="price"]/@id'))
            gid_list.append(gid)
            gname_dict[gid] = name
            item_num += 1

        self.next_page(hxs)
        return item_num

    def next_page(self, hxs):
        current = hxs.select('//div[@id="bottom_pagenum"]/span[@class="current"]/text()')
        total = hxs.select('//div[@id="bottom_pagenum"]/span[@class="numGo"]/text()').extract()
