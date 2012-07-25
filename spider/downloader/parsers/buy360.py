#/bin/python
# -*- coding: utf-8 -*-

import Image
from cStringIO import StringIO
from scrapy.selector import HtmlXPathSelector
from scrapy import log

from downloader.parsers.baseparser import BaseParser
from downloader.utils.selector import extract_value
from downloader.utils.ocr import gocr

#http://www.360buy.com/allSort.aspx
#no need to crawl following categories
#http://mvd.360buy.com/mvdsort/4051.html　音乐分类
#http://mvd.360buy.com/mvdsort/4052.html　影视分类
#http://mvd.360buy.com/mvdsort/4053.html  教育音像
#http://book.360buy.com/book/booksort.aspx 图书
class Buy360Parser(BaseParser):
    ALLOW_CGS =['buy360', ]

    def process_entrypage(self):
        link_num = 0
        hxs = HtmlXPathSelector(self.response)
        links = hxs.select('//div[contains(@id, "JDS_")]')
        for index, link in enumerate(links):
            cat1 = extract_value(link.select('div[@class="mt"]/h2/a/text()'))
            dls = link.select('div[@class="mc"]/dl[@class="fore"]')
            for dl in dls:
                cat2 = extract_value(dl.select('dt/a/text()'))
                dds = dl.select('dd/em') 
                for dd in dds:
                    cat3 = extract_value(dd.select('a/text()'))
                    url = dd.select('a/@href').extract()[0]
                    request = self.make_request_from_response(
                        url, prod_cats=[cat1, cat2, cat3],
                        cur_idepth=self.basic_link_info.cur_idepth,
                        )
                    self.crawl(request) 
                    link_num += 1

        return link_num

    def process_listpage(self):
        link_num = 0
        hxs = HtmlXPathSelector(self.response)
        skus = hxs.select('//li[@sku]')
        for sku in skus:
            skuvalue = ''.join(sku.select('@sku').extract())
            img_url = sku.select('div[@class="p-price"]/img/@src').extract()[0]
            prod_url = sku.select('div[@class="p-name"]/a/@href').extract()[0]
            prod_name = extract_value(sku.select('div[@class="p-name"]/a/text()'))
            request = self.make_request_from_response(\
                img_url,
                cur_idepth=self.basic_link_info.cur_idepth,
                prod_url=prod_url, prod_name=prod_name, sku=skuvalue
                )
            self.crawl(request)
            link_num += 1

        self.crawl_next_page()
        return link_num

    def next_page(self):
        hxs = HtmlXPathSelector(self.response)
        urls = hxs.select('//div[@class="pagin pagin-m"]/a[@class="next"]/@href').extract()
        if urls:
            return urls[0]
        else:
            return None
