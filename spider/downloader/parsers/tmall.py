#/bin/python
#coding: utf8

from scrapy.selector import HtmlXPathSelector
from scrapy.utils.signal import send_catch_log
from scrapy.project import crawler
from scrapy.http import Request
from scrapy import log

from downloader.clients.upyun import UpYun,md5,md5file
from downloader.clients.mymongo import MongoClient
from downloader.parsers.baseparser import BaseParser
from downloader.utils.selector import extract_value
from downloader.utils.product import canonicalize_price
from downloader.utils.url import get_uid
from downloader import signals

class TmallParser(BaseParser):
    ALLOW_CGS =['tmall', ]
    
    def __init__(self, spider, dbsettings, upyunsettings, config_file_dir):
        super(TmallParser, self).__init__(spider)

        self.upyun_client = UpYun(upyunsettings['bucket'], 
                upyunsettings['username'],
                upyunsettings['password'])

        self.mongo = MongoClient.from_settings(dbsettings)
        self.mongo.open()
    
    @classmethod
    def from_settings(cls, settings, spider):
        dbsettings = settings['MONGODB']
        upyunsettings = settings['UPYUN']
        config_file_dir = settings['CONFIG_FILE_DIR']
        return cls(spider, dbsettings, upyunsettings, config_file_dir)

    def parse(self, response):
        int_dep = response.request.meta.get("INT_DEP", None)
        req_type = response.request.meta.get("type", None)
        try:
            if req_type == 'image':
                self.log('process image, url:%s' % response.url,
                        level=log.DEBUG)
                #print response.headers
                directory='/tmall/%s' % response.request.meta.get('image_key')
                self.upyun_client.setContentMD5(md5(response.body)) 
                u = self.upyun_client.writeFile(directory, response.body,
                        auto=True)
                self.log('save image to upyun: %s, %s' % (directory, u))
        except Exception as e:
            self.log("exception: %s" % e, level=log.ERROR)
            import traceback
            self.log(traceback.format_exc(), level=log.ERROR)
            
    def process_entrypage(self):
        link_num = 0
        hxs = HtmlXPathSelector(self.response)
        brandlist_pattern = "//div[@class='brandList']/dl/dd"
        brandlist = hxs.select(brandlist_pattern)
        for item in brandlist:
            links = item.select('a')
            for link in links:
                url = link.select('./@href').extract()
                brand = link.select('./@title').extract()
                #print url, brand
                if url and brand:
                    request = self.make_request_from_response(
                            url, brand=brand,
                            cur_idepth=self.basic_link_info.cur_idepth,
                        )
                    self.crawl(request)
                    link_num += 1
                else:
                    self.log('Error: url %s, brand %s' % \
                        (' '.join(url), ' '.join(brand)), level=log.ERROR)
        return link_num

    def process_listpage(self):
        hxs = HtmlXPathSelector(self.response)
        nextpage = hxs.select("//a[@class='page-next']/@href")
        if nextpage:
            self.log('parse nextpage %s' % nextpage, level=log.DEBUG)
            nextpage = nextpage[0].extract()
            print nextpage
            meta ={'INT_DEP' : 1, 'from_url' : response.url, \
                    'brand' : response.request.meta.get('brand')}
            request = Request(url=nextpage, meta=meta)
            crawler.engine.crawl(request, self)
            self.log('nextpage %s' % nextpage, level=log.DEBUG)

        link_num = 0
        product_list = \
            hxs.select("//div[@id='J-listContainer']/form/ul[@class='product-list']/li")
        for item in product_list:
            product_info = item.select("div[@class='productInfo']")
            tmall_price = \
                extract_value(product_info.select("p/strong[@class='tmall-price']/text()"))
            prod_price = \
                extract_value(product_info.select("p/del[@class='proDefault-price']/text()"))
            prod_url = \
                extract_value(product_info.select("h3[@class='product-title']/a/@href"))
            prod_name = \
                extract_value(product_info.select("h3[@class='product-title']/a/text()"))
            prod_tags = \
                extract_value(product_info.select("p[@class='product-attr']/a/text()"))
            img_url = \
                extract_value(product_info.select("div[@class='product-img']/a/img/@data-ks-lazyload"))
            img_url = self._normalize_image_url(img_url)
            if image_url:
                request = self.make_request_from_response(
                        img_url,
                        cur_idepth=self.basic_link_info.cur_idepth,
                        prod_url=prod_url, prod_name=prod_name,
                        tmall_price=tmall_price, prod_price=prod_price,
                        prod_tags=prod_tags,
                    )
                self.crawl(request)
                link_num += 1
        
        self.crawl_next_page()
        return link_num

    def next_page(self):
        url = None
        hxs = HtmlXPathSelector(self.response)
        nextpage = hxs.select("//a[@class='page-next']/@href")
        if nextpage:
            url =  extract_value(nextpage[0])
        return url

    def process_contentpage(self):
        signature = self.sign_img_url(self.response.url) 
        directory='/tmall/%s' % signature 
        self.upyun_client.setContentMD5(md5(response.body))
        u = self.upyun_client.writeFile(directory, response.body,
                auto=True)
        self.log('save image to upyun: %s, %s' % (directory, u))

        prod_url = self.response.meta['prod_url']
        prod_name = self.response.meta['prod_name']
        prod_price = canonicalize_price(self.response.meta['prod_price'])
        tmall_price = self.response.meta['tmall_price']
        tmall_price = canonicalize_price(tmall_price.split('-')[0])
        prod_tags = self.response.meta['prod_tags']
        brand = self.response.meta['brand']

        #category = self.cgr.get_category(prod_name)
        #extracted_tags = self.cgr.get_tag(prod_name)
        #tags = "%s %s" % (prod_tags, extracted_tags)
        
        doc = {
                'id' : uid,
                'prod_url' : prod_url,
                'prod_name' : prod_name,
                #'prod_cat' : [category,],
                'prod_price' : prod_price,
                'tmall_price' : tmall_price,
                'prod_brand' : brand,
                'prod_img' : signature, 
                'prod_tags' : tags, 
            }
        self.mongo.insert(
            doc,
            pk=uid,
            collection=self.plg_mapping['tmall']
        )
        send_catch_log(signal=signals.kele_record_saved, doc=doc) 
    
    def sign_img_url(self, image_url):
        image_type = image_url.split('.')[-1]
        print "Image: %s, %s" %(image_url, image_type)
        return "%s.%s" % (get_uid(image_url), image_type)

    def _normalize_image_url(self, image_url):
        image_type = image_url.split('.')[-1]
        if image_type not in ('jpg', 'png'):
            self.log("bad image type:%s, url:%s" % (image_type, image_url),
                    level=log.ERROR)
            return None

        suffix = '_b.jpg'
        pos = image_url.rfind(suffix)
        if pos + len(suffix) == len(image_url):
            return image_url[0:pos]
        return image_url
