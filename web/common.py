#! /bin/sh
#-*- coding: utf-8 -*-
import md5, re

def md5sum(content):
    ins = md5.new()
    ins.update(content)
    return ins.hexdigest()

def url_normalize(url, site="360buy"):
    rule_360buy = '(http://www.360buy.com/product/\d+\.html)'
    s = re.match(rule_360buy, url)
    if s == None:
        return None
    return s.group(1)
