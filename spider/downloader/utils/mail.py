#!/usr/bin/env python
# -*- coding: utf-8 -*-
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class EmailClient(object):
    def __init__(self, host, user, pwd, fromaddr):
        self.host = host
        self.user = user
        self.pwd = pwd
        self.fromaddr = fromaddr

    @classmethod
    def from_settings(cls, settings):
        host = settings['host']
        user = settings['user']
        pwd = settings['pwd']
        fromaddr = settings['from']
        return cls(host, user, pwd, fromaddr)

    def send(self, recipients, subject, content):
        if not isinstance(recipients, list):
            raise Exception('expect a recipients list, got %s' %
                type(recipients))

        msg = MIMEMultipart('alternative')
        #msg = MIMEText(content, 'html')
        msg['Subject'] = subject
        msg['From'] = self.user 
        msg['To'] = ";".join(recipients)

        part3 = MIMEText(content, 'html')
        msg.attach(part3)
        try:
            server = smtplib.SMTP()
            server.connect(self.host)
            server.starttls() 
            server.login(self.user, self.pwd)
            server.sendmail(self.fromaddr, recipients, msg.as_string())
            server.quit()
        except Exception:
            raise

if __name__ == '__main__':
    host = "smtp.gmail.com:587"
    user = "smartbuyer.me"
    pwd = "smart1234"
    fromaddr = "smartbuyer.me@gmail.com"
    client = EmailClient(host, user, pwd, fromaddr)
    client.send(['lijian2@myhexin.com',], 'test mail', 'this a test mail from py')
