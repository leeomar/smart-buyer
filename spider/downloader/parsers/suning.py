#/bin/python
# -*- coding: utf-8 -*-
from scrapy.selector import HtmlXPathSelector
from downloader.parsers.baseparser import BaseParser
from downloader.utils.selector import extract_value

class SuningParser(BaseParser):
    ALLOW_CGS =['suning', ]

    def process_entrypage(self):
        link_num = 0
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
                    url, prod_cats=[cat1, cat2],
                    cur_idepth=self.basic_link_info.cur_idepth,
                    )
                self.crawl(request) 
                link_num += 1

        return link_num

    def process_listpage(self):
        link_num = 0
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
            )
            self.crawl(request)
            link_num += 1

        self.crawl_next_page()
        return link_num

    def next_page(self):
        url = None
        hxs = HtmlXPathSelector(self.response)
        last_page = int(extract_value(hxs.select('//a[@id="pageLast"]/text()')))
        current_page = int(extract_value(
            hxs.select('//div[@class="snPages"]/a[@class="current"]/text()')))

        if current_page == 1:
            fs = self.response.url.split('/')[-1].split('_')
            url = "http://www.suning.com/emall/secondPointSearchNewCmd?"\
                "storeId=%s&catalogId=%s&categoryId=%s&topBrandName="\
                "&top=N&top_category=%s&sortIndex=5&currentPage=1&isList=0"\
                % (fs[1], fs[2], fs[-2], fs[-3],)
        elif current_page < last_page:
            url = self.response.url.replace(
                'currentPage=%s' % (current_page-1), 'currentPage=%s' % current_page)

        return url
