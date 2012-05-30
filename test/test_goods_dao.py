#/bin/python
# -*- coding: utf-8 -*-

from price_trend.dao.goods_dao import GoodsDAO 

if __name__ == '__main__':
    goods_dao = GoodsDAO('127.0.0.1', 27017, "test", "test")

    url = 'http://www.360buy.com/product/342079.html'
    name = "moto手机"
    cat = "手机"
    price = 1599

    goods_dao.add(url, name, cat, price)

    price = 1498
    goods_dao.add(url, name, cat, price)
