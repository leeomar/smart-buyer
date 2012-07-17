#/bin/python
# coding: utf8
'''
this module is used to record spider status, statistic

'''

class SpiderInfo(object):
    
    def __init__(self):
        self.status = 'busy' # busy, idle, error
        self.processed_task = 0
        self.running_task = 0
        self.regist_time = None #注册时间　
        self.work_time = None #工作时间
        self.idle_time = None #空闲时间

    def update(self):
        pass

class Slot(object):
    
    def __init__(self):
        self.register_spiders = {} # spiderid : spiderInfo


class StatsEngine(object):
    
    def __init__(self):
        pass

    def update(self, spider, task_num, work_time):
        '''
            task info will be store in mongodb:
                {
                    "_id" : ObjectID,
                    "domain" : 360.com,
                    "date_time" : 2012-05-12,
                    "crawl_pages" : xxx,
                }
        '''
        pass
