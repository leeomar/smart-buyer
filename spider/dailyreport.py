#!/bin/python
import datetime
from downloader.extensions.statistic import StatisticInfo
from downloader.utils.mail import EmailClient
from GChartWrapper import *
from GChartWrapper.encoding import Encoder
from GChartWrapper.constants import PY_VER,_print, COLOR_MAP

MAIL_SETTING = {
    'host' : 'smtp.gmail.com:587',
    'user' : 'smartbuyer.me',
    'pwd' : 'smart1234',
    'from' : 'smartbuyer.me@gmail.com',
    'recipients' : ['lijian.whu@gmail.com', ],
}

REDIS_SETTING = {
    'host' : '127.0.0.1',
    'port' : 6379,
    'db' : 0,
    'default_expire' : 0,
}

class DLDailyReport(object):
    def __init__(self, redis_settings, mail_settings):
        self.statistic = StatisticInfo(redis_settings)
        self.mail = EmailClient.from_settings(mail_settings)
        self.recipients = mail_settings['recipients']

    def sendreport(self, msg):
        self.mail.send(self.recipients, 'SmartBuyer daily report', msg)

    def last_week_iterator(self, ):
        for i in range(-7, 0):
            dt = datetime.date.today() + datetime.timedelta(i)
            yield dt.strftime('%Y%m%d') 

    def genchart(self, data):
        G = LineXY([])
        G.title('SmartBuyer Daiyly Report')
        G.size(600, 300)
        G.axes.type('xyx')
        G.axes.label(0, 1, 7) # X Axis
        G.axes.range(1, 0, 100)
        G.axes.label(2, *[item for item in self.last_week_iterator()])

        lines = []
        legends = []
        for key, value in data.items():
            lines.append(['-1',])
            lines.append(value)
            legends.append(key)

        G.dataset(lines)
        G.legend(*legends)
       
        G.color(*(COLOR_MAP.values()[:len(data)]))
        for i in range(0, len(data)):
            G.marker('s', 'blue', i, -1, 5)
        print G
        return str(G) 
    '''
        report:
                 8.1     8.2     8.3   ...
        360buy   40/109    

    '''
    def run(self):
        '''
        result = {
            '360buy.com' : {
                    '2012-07-18' : (2068, 3400), # 2068 is saved records num,
                                                 # 3400 is extracted records
                                                 # num
                    '2012-07-19' : (3011, 5400),
                    ...
                }

        }
        '''
        result = {}
        for strtime in obj.last_week_iterator():
            temp = {} 
            saved_records = self.statistic.get_record_saved(strtime)
            for domain, value in saved_records.items():
                if domain not in result:
                    result[domain] = {} 
                result[domain][strtime] = [value]

            extracted_records = self.statistic.get_record_extracted(strtime)
            for domain, value in extracted_records.items():
                if domain not in result:
                    result[domain] = {} 
                    result[domain][strtime] = [0, value]
                elif strtime not in result[domain]:
                    result[domain][strtime] = [0, value]
                else:
                    result[domain][strtime].append(value)

        header = "".join(["<td>%s</td>" % item for item in obj.last_week_iterator()])
        table = "<html><head></head><body><table border=1><tr><td></td>%s</tr>" % header
        chartdata = {}
        for domain, record in result.items():
            array1 = []
            array2 = []
            row = "<tr><td>%s</td>" % domain
            for strtime in obj.last_week_iterator():
                if strtime in record:
                    data = "%s/%s" % (record.get(strtime)[0],
                            record.get(strtime)[1])
                    array1.append(float(record.get(strtime)[0])/100)
                    array2.append(float(record.get(strtime)[1])/100)
                else:
                    data = "None/None"
                    array1.append(0)
                    array2.append(0)
                row = "%s<td>%s</td>" % (row, data)
            chartdata['%s saved' % domain] = array1
            chartdata['%s extracted' % domain] = array2
            table = "%s%s</tr>" % (table, row)

        img = "<img src=\"%s\">" % self.genchart(chartdata).replace("&", "&amp;")
        table = "%s</table><p>%s</p></body></html>" % (table, img)
        self.sendreport(table)

if __name__ == '__main__':
    obj = DLDailyReport(REDIS_SETTING, MAIL_SETTING)
    obj.run()
    print 'done'
