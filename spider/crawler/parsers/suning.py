#/bin/python
# -*- coding: utf-8 -*-

import Image
from cStringIO import StringIO
from scrapy.selector import HtmlXPathSelector
from scrapy import log

from crawler.parsers.baseparser import BaseParser
from crawler.utils.selector import extract_value
from crawler.utils.ocr import gocr
from crawler.utils.url import get_uid

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
            prod_name = \
                extract_value(prod.select('div[@class="inforBg"]/span/a/@title'))
            prod_url = \
                extract_value(prod.select('div[@class="inforBg"]/span/a/@href'))
            
            img_url = \
                extract_value(prod.select('div[@class="inforBg"]/p/img/@src'))

            request = self.make_request_from_response(\
                img_url,
                cur_idepth=self.basic_link_info.cur_idepth,
                prod_url=prod_url, prod_name=prod_name, 
                cat = self.response.meta['cat']
            )
            self.crawl(request)

            item_num += 1

        self.next_page(hxs)
        return item_num

    def process_detailpage(self):
        prod_url = self.response.meta['prod_url']
        prod_name = self.response.meta['prod_name']
        cat = self.response.meta['cat']

        uid = get_uid(self.response.url)
        image = Image.open(StringIO(self.response.body))
        image_file = "%s/%s.%s" % (self.tmpfile_dir, uid, image.format.lower())
        image.save(image_file)
        price = gocr(image_file)
        log.msg('save image:%s, url:%s, price:%s' \
            %(image_file, self.response.url, price))

        self.save(prod_url, prod_name, cat, price)
        return 0

    def next_page(self, hxs):
        url = None
        last_page = int(extract_value(hxs.select('//a[@id="pageLast"]')))
        current_page = int(extract_value(hxs.select('//div[@class="snPages"]/a[@class="current"]/text()').extract()))
        if current_page == 1:
            #http://www.suning.com/emall/pcd_10052_10051_-7_N_20089_20002_.html
            #['pcd', '10052', '10051', '-7', 'N', '20089', '20002', '.html']
            fs = self.response.url.split('/')[-1].split('_')
            url = "http://www.suning.com/emall/secondPointSearchNewCmd?"\
                "storeId=%s&catalogId=%s&categoryId=%s&topBrandName="\
                "&top=N&top_category=%s&sortIndex=5&currentPage=1&isList=0"\
                % (fs[1], fs[2], fs[-2], fs[-3],)
        elif current_page < last_page:
            url = self.response.url.replace('currentPage=%s' % (current_page-1), 'currentPage=%s' % current_page)

        if url:
            request = self.make_request_from_response(
                url=url,)
            self.crawl(request, cat=self.response.meta['cat'])
            self.log('next page:%s' % request.url)
