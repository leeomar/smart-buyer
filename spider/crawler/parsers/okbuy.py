#/bin/python

from .baseparser import BaseParser
from scrapy.selector import HtmlXPathSelector

from crawler.utils.selector import extract_value
from crawler.utils.goods import canonicalize_price
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
    BASE_URL = "http://www.okbuy.com"
    DETAIL_BASE_URL = "http://www.okbuy.com/product/detail/"
    PRICE_REQUST_URL = "http://www.okbuy.com/product/ajax_find_listprice/"

    def process(self):
        cur_idepth = self.basic_link_info.cur_idepth
        if cur_idepth == 1:
            return self.process_listpage()
        else:
            return self.process_detailpage()

    def process_listpage(self):
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

        request = self.make_request_from_response(
            url= "%s%s" % (self.PRICE_REQUST_URL, ",".join(gid_list)),
            cur_idepth=self.basic_link_info.cur_idepth,
            gname_dict=gname_dict,
            )
        self.crawl(request)

        self.next_page(hxs)
        return item_num
    
    def process_detailpage(self):
        jsonobj = json.loads(self.response.body, self.response.encoding)
        gname_dict = self.response.meta['gname_dict']
        for key in gname_dict:
            self.log("%s, type:%s" %(jsonobj.get(key), type(jsonobj.get(key))))
            if key not in jsonobj:
                self.log("fail get price for %s" % key, level=log.ERROR)
                continue

            price = canonicalize_price(jsonobj.get(key))
            url = "%s%s.html" % (self.DETAIL_BASE_URL, key)
            name = gname_dict[key]
            self.save(url, name, [], price)
        return len(gname_dict)

    def next_page(self, hxs):
        #pagination object area
        poa = hxs.select('//div[@id="bottom_pagenum"]/span/a')
        for item in poa:
            text = extract_value(item.select('text()'))
            if text.find('下一页') != -1:
                url = extract_value(item.select('@href'))
                request = self.make_request_from_response(
                    url="%s%s" % (self.BASE_URL, url),
                    )
                self.crawl(request)
                self.log('next page:%s' % request.url)
                break
