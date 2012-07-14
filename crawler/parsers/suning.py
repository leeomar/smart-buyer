#/bin/python
# -*- coding: utf-8 -*-

import Image
from cStringIO import StringIO
from scrapy.selector import HtmlXPathSelector
from scrapy import log

from crawler.parsers.baseparser import BaseParser
from crawler.utils.selector import extract_value
from crawler.utils.ocr import gocr

class SuningParser(BaseParser):
    BASE_URL = 'http://www.suning.com'
    ALLOW_CGS =['suning', ]

    def process(self):
        cur_idepth = self.basic_link_info.cur_idepth
        if cur_idepth == 1:
            return self.process_entrypage()
        elif cur_idepth == 2:
            return self.process_listpage()
        else:
            return self.process_detailpage()

    def process_entrypage(self):
        item_num = 0
        hxs = HtmlXPathSelector(self.response)
        floors = hxs.select('//div[@class="sFloors l"]/div[@class="sFloor clearfix"]')
        #we don't need floor[0], which is book
        for i in range(1, len(floors)):
            cat1 = extract_value(floors[i].select('h3/a/text()'))
            
            subcats = floors[i].select('ul/li/dl/dt')
            for subcat in subcats:
                cat2 = extract_value(subcat.select('a/text()'))
                url = extract_value(subcat.select('a/@href'))
                request = self.make_request_from_response( \
                    "http://www.360buy.com/%s"%url,
                    cur_idepth=self.basic_link_info.cur_idepth,
                    cat=[cat1, cat2])
                self.crawl(request) 
                item_num += 1

        return item_num

    def process_listpage(self):
        item_num = 0
        hxs = HtmlXPathSelector(self.response)
        products = hxs.select('//div[@id="proShow"]/ul/li')
        for prod in products:
            prod_title = \
                extract_value(prod.select('div[@class="inforBg"]/span/a/@title'))
            prod_url = \
                extract_value(prod.select('div[@class="inforBg"]/span/a/@href'))
            
            img_url = \
                extract_value(prod.select('div[@class="inforBg"]/p/img/@src'))

            request = self.make_request_from_response(\
                img_url,
                cur_idepth=self.basic_link_info.cur_idepth,
                prod_url=prod_url, prod_title=prod_title, 
                cat = self.response.meta['cat']
            )
            self.crawl(request)

            item_num += 1

        self.next_page(hxs)
        return item_num

    def process_detailpage(self):
        sku = self.response.meta['sku']
        gurl = self.response.meta['gurl']
        name = self.response.meta['name']
        cat = self.response.meta['cat']

        image = Image.open(StringIO(self.response.body))
        image_file = "%s/%s.%s" % (self.tmpfile_dir, sku, image.format.lower())
        image.save(image_file)
        price = gocr(image_file)
        log.msg('save image:%s, url:%s, price:%s' \
            %(image_file, self.response.url, price))

        self.save(gurl, name, cat, price)
        return 0

    def next_page(self, hxs):
        urls = hxs.select('//div[@class="pagin pagin-m"]/a[@class="next"]/@href').extract()
        if urls:
            request = self.make_request_from_response(
                url="http://www.360buy.com/products/%s" % urls[0],)
            self.crawl(request)
            self.log('next page:%s' % request.url)
