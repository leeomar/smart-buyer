#!/usr/bin/env python
# -*- coding: utf-8 -*-
import smtplib
from email.mime.text import MIMEText

class EmailClient(object):

    def __init__(self, serveraddr, user, pwd, fromaddr):
        self.serveraddr = serveraddr
        self.user = user
        self.pwd = pwd
        self.fromaddr = fromaddr

    def send(self, recipients, subject, content):
        #me=mail_user+"<"+mail_user+"@"+mail_postfix+">"
        msg = MIMEText(content, 'html')
        msg['Subject'] = subject
        msg['From'] = self.user 
        msg['To'] = ";".join(recipients)
        try:
            server = smtplib.SMTP()
            server.connect(self.serveraddr)
            #server.starttls() 
            server.login(self.user, self.pwd)
            server.sendmail(self.fromaddr, recipients, msg.as_string())
            server.close()
        except Exception:
            raise

if __name__ == '__main__':
    serveraddr = "smtp.gmail.com:587"
    user = ""
    pwd = ""
    fromaddr = "lijian.whu@gmail.com"
    client = EmailClient(serveraddr, user, pwd, fromaddr)
    client.send(['lijian2@myhexin.com',], 'test mail', 'this a test mail from py')
