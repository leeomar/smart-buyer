#!/usr/bin/env python
#coding : utf8

import sys
sys.path.append('../gen-py.twisted')

from scheduler.ttypes import Seed, SeedsPackage, JobReport

def assert_type(instance, expect_type):
    if not isinstance(instance, expect_type):
        raise Exception("unexpect type:%s, only %s is accepted" % (type(instance, expect_type)))

def format_seed(seed):
    assert_type(seed, Seed)
    return "Seed[url:%s, content_group:%s, pl_group:%s, max_idepth:%s, max_xdepth:%s, cur_idepth:%s, cur_xdepth:%s, priority:%s, crawl_interval:%s]" \
        % (seed.url, seed.content_group, seed.pl_group, 
            seed.max_xdepth, seed.max_xdepth, 
            seed.cur_idepth, seed.cur_xdepth,
            seed.priority, seed.crawl_interval)

def format_seedspackage(pkg):
    assert_type(pkg, SeedsPackage)
    return "SeedsPackage[ID:%s, %s]" % \
        (pkg.ID, ','.join([str(seed) for seed in pkg.seeds]))

def format_jobreport(report):
    assert_type(report, JobReport)
    return "JobReport[spiderid:%s, work_time:%s, idle_time:%s, fail_url_num:%s, crawled_url_num:%s, crawled_page_size:%s]" % \
        (report.spiderid, report.work_time, 
         report.idle_time, report.fail_url_num, 
         report.crawled_url_num, report.crawled_page_size)
