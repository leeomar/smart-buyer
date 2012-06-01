#/bin/python
# -*- coding: utf-8 -*-

from scrapy.selector import HtmlXPathSelector
from scrapy.utils.signal import send_catch_log
from scrapy import log

from crawler.parsers.baseparser import BaseParser
from crawler.utils.selector import extract_value
from crawler.utils.ocr import gocr
from crawler import signals

#http://www.360buy.com/allSort.aspx
#no need to crawl following categories
#http://mvd.360buy.com/mvdsort/4051.html　音乐分类
#http://mvd.360buy.com/mvdsort/4052.html　影视分类
#http://mvd.360buy.com/mvdsort/4053.html  教育音像
#http://book.360buy.com/book/booksort.aspx 图书
class Buy360Parser(BaseParser):
    ALLOW_CGS =['buy360', ]

    def process(self):
        #self.log('got %s, base url:%s' \
        #    % (self.response.url, get_base_url(self.response)))
        if self.basic_link_info.cur_idepth == 1:
            self.process_entrypage()
        else:
            self.process_listpage()

    def process_entrypage(self):
        item_num = 0
        hxs = HtmlXPathSelector(self.response)
        links = hxs.select('//div[contains(@id, "JDS_")]')
        for index, link in enumerate(links):
            #cat1 = ''.join(
            #    self.encode(link.select('div[@class="mt"]/h2/a/text()').extract()))
            cat1 = extract_value(link.select('div[@class="mt"]/h2/a/text()'))
            dls = link.select('div[@class="mc"]/dl[@class="fore"]')
            for dl in dls:
                #cat2 = ''.join(self.encode(dl.select('dt/a/text()').extract()))
                cat2 = extract_value(dl.select('dt/a/text()'))
                dds = dl.select('dd/em') 
                for dd in dds:
                    #cat3 = ''.join(self.encode(dd.select('a/text()').extract()))
                    cat3 = extract_value(dd.select('a/text()'))
                    catlist = (cat1, cat2, cat3)
                    url = dd.select('a/@href').extract()[0]
                    request = self.make_request_from_response( \
                        "http://www.360buy.com/%s"%url,
                        cur_idepth=self.basic_link_info.cur_idepth,
                        cat=catlist)
                    self.crawl(request) 
                    item_num += 1

        send_catch_log(signal=signals.item_extracted,
            url=self.response.url, item_num=item_num)

    def process_listpage(self):
        item_num = 0
        hxs = HtmlXPathSelector(self.response)
        skus = hxs.select('//li[@sku]')
        for sku in skus:
            img = sku.select('div[@class="p-price"]/img/@src').extract()[0]
            price = gocr(img, self.tmpfile_dir)
            if price <= 0:
                self.log('gocr %s from %s' % (price, img), level=log.ERROR)
                continue

            url = sku.select('div[@class="p-name"]/a/@href').extract()[0]
            name = extract_value(sku.select('div[@class="p-name"]/a/text()'))
            cat = self.response.meta['cat']
            self.spider.dbclient.put(url, name, cat, price,
                self.get_collection_name())
            item_num += 1
            #send_catch_log(signal=signals.extract_goods,
            #    url=url, price=price, name=name, cat=cat)

        self.next_page(hxs)
        send_catch_log(signal=signals.item_extracted,
            url=self.response.url, item_num=item_num)

    def next_page(self, hxs):
        urls = hxs.select('//div[@class="pagin pagin-m"]/a[@class="next"]/@href').extract()
        if urls:
            request = self.make_request_from_response(
                url=urls[0],)
            self.crawl(request)
            self.log('next page:%s' % request.url)
