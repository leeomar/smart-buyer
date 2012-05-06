#! /bin/sh
#-*- coding: utf-8 -*-
import md5
def md5sum(content):
	ins = md5.new()
	ins.update(content)
	return ins.hexdigest()
