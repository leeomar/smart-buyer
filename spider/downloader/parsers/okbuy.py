#/bin/python
# -*- coding: utf-8 -*-

import Image
from cStringIO import StringIO
from scrapy.selector import HtmlXPathSelector
from scrapy import log

from downloader.utils.product import canonicalize_price
from downloader.parsers.baseparser import BaseParser
from downloader.utils.selector import extract_value
import json

#http://www.360buy.com/allSort.aspx
#no need to crawl following categories
#http://mvd.360buy.com/mvdsort/4051.html　音乐分类
#http://mvd.360buy.com/mvdsort/4052.html　影视分类
#http://mvd.360buy.com/mvdsort/4053.html  教育音像
#http://book.360buy.com/book/booksort.aspx 图书
class OkbuyParser(BaseParser):
    ALLOW_CGS =['okbuy', ]
    DETAIL_BASE_URL = "http://www.okbuy.com/product/detail/"
    PRICE_REQUST_URL = "http://www.okbuy.com/product/ajax_find_listprice/"
    LINK_DEPTH_METHODS = {1: "process_entrypage", 
        2: 'process_listpage', 3: 'process_ajax_price'}

    def process_entrypage(self):
        link_num = 0
        hxs = HtmlXPathSelector(self.response)
        rows = hxs.select("//div[@class='t-abcconr']")
        for row in rows:
            links = row.select("a")
            for link in links:
                url = extract_value(link.select('@href'))
                brand = extract_value(link.select('p/text()'))
                request = self.make_request_from_response(
                    url, brand=brand,
                    cur_idepth=self.basic_link_info.cur_idepth,
                    )
                self.crawl(request)
                link_num += 1
        return link_num

    def process_listpage(self):
        link_num = 0
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
            link_num += 1

        request = self.make_request_from_response(
            url= "%s%s" % (self.PRICE_REQUST_URL, ",".join(prod_ids)),
            cur_idepth=self.basic_link_info.cur_idepth,
            prod_id2names=prod_id2names,
            )

        self.crawl(request)
        self.crawl_next_page()
        return link_num

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
