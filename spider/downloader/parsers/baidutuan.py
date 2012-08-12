#/bin/python
# -*- coding: utf-8 -*-

import Image
from cStringIO import StringIO
from scrapy.selector import HtmlXPathSelector
from scrapy import log

from downloader.parsers.baseparser import BaseParser
from downloader.utils.selector import extract_value
from downloader.utils.ocr import gocr

#http://tuan.baidu.com/?sp=1&page=1#main
class BaiduTuanParser(BaseParser):
    ALLOW_CGS =['baidu_tuan', ]

    def process_listpage(self):
        link_num = 0
        hxs = HtmlXPathSelector(self.response)
        #hxs.select("//div[@id='content']/div[@class='goods']/div[@class='wt-good-item']")
        prods = hxs.select("//div[@id='content']/div[@class='goods']/div[@class='wt-good-item']")
        for prod in prods:
            site = extract_value(prod.select("div[@class='mbs good-item-title']/a")[0].select("text()")) 
            prod_url = extract_value(prod.select("div[@class='mbs good-item-title']/a")[1].select("@href").extract()[0]) 
            prod_name = extract_value(prod.select("div[@class='mbs good-item-title']/a")[1].select("text()")) 
            img_url = extract_value(prod.select("div[@class='mbm good-item-img']/a/img/@src"))
            
            #TODO
            prod_price = extract_value(prod.select("div[@class='good-item-info']/p/span[@class='price']/text()"))

            link_num += 1

        self.crawl_next_page()
        return link_num

    def next_page(self):
        hxs = HtmlXPathSelector(self.response)
        #//div[@id='pagelist']/a[@class='next-page-a']/@href
        urls = hxs.select("//div[@id='pagelist']/a[@class='next-page-a']/@href").extract()
        if urls:
            return urls[0]
        else:
            return None
