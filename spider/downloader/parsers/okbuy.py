#/bin/python

from .baseparser import BaseParser
from scrapy.selector import HtmlXPathSelector

from downloader.utils.selector import extract_value
from downloader.utils.product import canonicalize_price
from scrapy import log
import json

#http://www.okbuy.com/product/search?category=clothes 
#http://www.okbuy.com/product/search?category=child_shoes
#http://www.okbuy.com/product/search?category=bags

#http://www.okbuy.com/product/search
#http://www.okbuy.com/product/ajax_find_listprice/16970593,16978450
#http://www.okbuy.com/product/detail/16970593.html?ref=l
#http://www.okbuy.com/product/search?&per_page=100#listheader
class OkbuyParser(BaseParser):
    ALLOW_CGS = ['okbuy', ]
    #BASE_URL = "http://www.okbuy.com"
    DETAIL_BASE_URL = "http://www.okbuy.com/product/detail/"
    PRICE_REQUST_URL = "http://www.okbuy.com/product/ajax_find_listprice/"

    LINK_DEPTH_METHODS = {1: 'process_listpage', 2: 'process_ajax_price'}

    def process_listpage(self):
        item_num = 0
        hxs = HtmlXPathSelector(self.response)
        products = hxs.select('//div[@class="floorConn"]/div[@class="goodsList"]/ul/li')
        prod_id2names = {}
        prod_ids = []
        for item in products:
            name = extract_value(item.select('.//p[@class="productName"]/@title'))
            #url =  extract_value(item.select('div[@class="txt"]/a/@href'))
            prod_id = extract_value(item.select('.//span[@name="price"]/@id'))

            prod_ids.append(prod_id)
            prod_id2names[prod_id] = name
            item_num += 1

        request = self.make_request_from_response(
            url= "%s%s" % (self.PRICE_REQUST_URL, ",".join(prod_ids)),
            cur_idepth=self.basic_link_info.cur_idepth,
            prod_id2names=prod_id2names,
            )
        self.crawl(request)

        self.crawl_next_page()
        return item_num
    
    def process_ajax_price(self):
        jsonobj = json.loads(self.response.body, self.response.encoding)
        prod_id2names = self.response.meta['prod_id2names']
        for prod_id in prod_id2names:
            #self.log("%s, type:%s" %(jsonobj.get(prod_id), type(jsonobj.get(prod_id))))
            if prod_id not in jsonobj:
                self.log("fail get price for %s" % prod_id, level=log.ERROR)
                continue

            price = canonicalize_price(jsonobj.get(prod_id))
            prod_url = "%s%s.html" % (self.DETAIL_BASE_URL, prod_id)
            prod_name = prod_id2names[prod_id]
            self.save(prod_url, prod_name, [], price)
        return len(prod_id2names)

    def next_page(self, ):
        hxs = HtmlXPathSelector(self.response)
        poa = hxs.select('//div[@id="bottom_pagenum"]/span/a')
        for item in poa:
            text = extract_value(item.select('text()'))
            if text.find('下一页') != -1:
                url = extract_value(item.select('@href'))
                return url

        return None
