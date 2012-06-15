#!/usr/bin/env python
# -*- coding: utf-8 -*-
import smtplib
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

        message = MIMEText(content, 'html')
        message['Subject'] = subject
        message['From'] = self.user 
        message['To'] = ";".join(recipients)
        try:
            server = smtplib.SMTP()
            server.connect(self.host)
            #server.starttls() 
            server.login(self.user, self.pwd)
            server.sendmail(self.fromaddr, recipients, message.as_string())
            server.close()
        except Exception:
            raise

if __name__ == '__main__':
    host = "smtp.gmail.com:587"
    user = ""
    pwd = ""
    fromaddr = "lijian.whu@gmail.com"
    client = EmailClient(host, user, pwd, fromaddr)
    client.send(['lijian2@myhexin.com',], 'test mail', 'this a test mail from py')
