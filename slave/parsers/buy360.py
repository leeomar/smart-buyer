#/bin/python
# -*- coding: utf-8 -*-

from slave.parsers.basicparser import BasicParser

class Buy360Parser(BasicParser):
    allow_content_group = '360buy_default'

    def conditon_permit(self, response, basic_link_info, spider):
        if basic_link_info.content_group == Buy360Parser.allow_content_group:
            return True
        else:
            return False

    def process(self):
        pass

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