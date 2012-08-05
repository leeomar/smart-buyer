#!/bin/python
import datetime
from downloader.extensions.statistic import StatisticInfo
from downloader.utils.mail import EmailClient

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
        for i in range(-6, 0):
            dt = datetime.date.today() + datetime.timedelta(i)
            yield dt.strftime('%Y%m%d') 
    '''
        mail:
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
                else:
                    result[domain][strtime].append(value)

        header = "".join(["<td>%s</td>" % item for item in obj.last_week_iterator()])
        table = "<html><head></head><body><table border=1><tr><td></td>%s</tr>" % header
        for domain, record in result.items():
            row = "<tr><td>%s</td>" % domain
            for strtime in obj.last_week_iterator():
                if strtime in record:
                    data = "%s/%s" % (record.get(strtime)[0],
                            record.get(strtime)[1])
                else:
                    data = "None/None"
                row = "%s<td>%s</td>" % (row, data)

            table = "%s%s</tr>" % (table, row)
        img = "<img src='http://chart.apis.google.com/chart?chco=3072f3,FF0000,00aaaa&amp;chd=t:-1|20.0,70.0,80.0|-1|99.0,30.0,70.0|-1|10.0,90.0,10.0&amp;chdl=data1|data2|data3&amp;chds=0,100&amp;chm=s,FF0000,0,-1,5|s,0000FF,1,-1,5|s,00aa00,2,-1,5&amp;chs=300x150&amp;cht=lxy&amp;chtt=test+chart&amp;chxl=0:|6.9|6.10|6.11|1:|0|50|100&amp;chxt=x,y'></p></body></html>"
        table = "%s</table><p>%s</p></body></html>" % (table, img)
        self.sendreport(table)

if __name__ == '__main__':
    obj = DLDailyReport(REDIS_SETTING, MAIL_SETTING)
    obj.run()
