#!/bin/python
import datetime
from downloader.clients.statistic import StatisticInfo

class DLDailyReport(object):

    def __init__(self, redis_settings, ):
        self.statistic = StatisticInfo(redis_settings)
        self.data = {}
        self.domains = set()

    def add(self, strtime, domain, value):
        item = self.data.get(strtime)
        if item is None:
            item = {}
            self.data[strtime] = item
        item[domain] = value

    def run(self):
        for i in range(-7, -1):
            dt = datetime.date.today() + datetime.timedelta(i)
            strtime = dt.strftime('%Y%m%d')

            saved_records = self.statistic.get_record_saved(strtime)
            extracted_records = self.statistic.get_record_extracted(strtime)
            if extracted_records:
                for k, v in extracted_records.items():
                    num2 = saved_records.get(k, 0)
                    self.add(strtime, k, "%s/%s" % (num2, v))

    def sendreport(self):
        pass
