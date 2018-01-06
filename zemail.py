#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time    : 18/1/6 10:36
# Author  : Eric.Zhang

from sys import argv
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr


class ZabbixSendMail(object):
    def __init__(self, reciver, mail_subject, message):
        self.smtp_server_addr = "smtp.126.com"
        self.smtp_server_port = 465
        self.smtp_server_passwd = 'XXXX'

        self.sender = 'neteric@126.com'
        self.sender_mail_postfix = '126.com'

        self.sender_alias = "zabbix server"
        self.reciver = reciver
        self.reciver_alias = "system administrator"

        self.message = message
        self.mail_subject = mail_subject

    def mail(self):
        try:
            msg = MIMEText(self.message, 'plain', 'utf-8')
            msg['From'] = formataddr([self.sender_alias, self.sender])
            msg['To'] = formataddr([self.reciver_alias, self.reciver])
            msg['Subject'] = self.mail_subject

            server = smtplib.SMTP_SSL(self.smtp_server_addr,
                                      self.smtp_server_port)
            server.login(self.sender, self.smtp_server_passwd)
            server.sendmail(self.sender, self.reciver, msg.as_string())
            server.quit()
        except Exception as e:
            print e

if __name__ == "__main__":
    zsendmail = ZabbixSendMail(argv[1], argv[2], argv[3])
    zsendmail.mail()
