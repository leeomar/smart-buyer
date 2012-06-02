#/bin/python
# -*- coding: utf-8 -*-

import Image
from cStringIO import StringIO
from scrapy.selector import HtmlXPathSelector
from scrapy import log

from crawler.parsers.baseparser import BaseParser
from crawler.utils.selector import extract_value
from crawler.utils.ocr import gocr

#http://www.360buy.com/allSort.aspx
#no need to crawl following categories
#http://mvd.360buy.com/mvdsort/4051.html　音乐分类
#http://mvd.360buy.com/mvdsort/4052.html　影视分类
#http://mvd.360buy.com/mvdsort/4053.html  教育音像
#http://book.360buy.com/book/booksort.aspx 图书
class Buy360Parser(BaseParser):
    ALLOW_CGS =['buy360', ]

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
        links = hxs.select('//div[contains(@id, "JDS_")]')
        for index, link in enumerate(links):
            cat1 = extract_value(link.select('div[@class="mt"]/h2/a/text()'))
            dls = link.select('div[@class="mc"]/dl[@class="fore"]')
            for dl in dls:
                cat2 = extract_value(dl.select('dt/a/text()'))
                dds = dl.select('dd/em') 
                for dd in dds:
                    cat3 = extract_value(dd.select('a/text()'))
                    catlist = (cat1, cat2, cat3)
                    url = dd.select('a/@href').extract()[0]
                    request = self.make_request_from_response( \
                        "http://www.360buy.com/%s"%url,
                        cur_idepth=self.basic_link_info.cur_idepth,
                        cat=catlist)
                    self.crawl(request) 
                    item_num += 1

        return item_num
        #send_catch_log(signal=signals.item_extracted,
        #    url=self.response.url, item_num=item_num)

    def process_listpage(self):
        item_num = 0
        hxs = HtmlXPathSelector(self.response)
        skus = hxs.select('//li[@sku]')
        for sku in skus:
            skuvalue = ''.join(sku.select('@sku').extract())
            imgurl = sku.select('div[@class="p-price"]/img/@src').extract()[0]
            url = sku.select('div[@class="p-name"]/a/@href').extract()[0]
            name = extract_value(sku.select('div[@class="p-name"]/a/text()'))
            request = self.make_request_from_response(\
                imgurl,
                cur_idepth=self.basic_link_info.cur_idepth,
                gurl=url, name=name, sku=skuvalue
                )
            self.crawl(request)

            #price = gocr(img, self.tmpfile_dir)
            #if price <= 0:
            #    self.log('gocr %s from %s' % (price, img), level=log.ERROR)
            #    continue

            item_num += 1

        self.next_page(hxs)
        return item_num
        #send_catch_log(signal=signals.item_extracted,
        #    url=self.response.url, item_num=item_num)

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
