#/bin/python
# -*- coding: utf-8 -*-

from crawler.parsers.baseparser import BaseParser

class Buy360Parser(BaseParser):
    ALLOW_CGS =['buy360', ]

    def process(self):
        self.log('got %s' % self.response.url)

    #http://www.360buy.com/allSort.aspx
    #no need to crawl following categories
    #http://mvd.360buy.com/mvdsort/4051.html　音乐分类
    #http://mvd.360buy.com/mvdsort/4052.html　影视分类
    #http://mvd.360buy.com/mvdsort/4053.html  教育音像
    #http://book.360buy.com/book/booksort.aspx 图书
    def process_entrypage(self):
        pass

    def process_listpage(self):
        pass
