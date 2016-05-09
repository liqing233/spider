#! usr/bin/env python

"""
@author:liqing
@email:626924971@qq.com
@tel:18674450812
@create time:2016/5/9
@version:v1.0
function:send mail
"""

import sys
import smtplib
from email.mime.text import MIMEText
import ConfigParser

import logging
import logging.config

logging.config.fileConfig(r"../../configures/log/logger.conf")
logger = logging.getLogger(__name__)

class sendmail(object):
    def __init__(self,text,subject,config = r"../../configures/email/email.conf"):
        cf = ConfigParser.ConfigParser()
        cf.read(config)
        self.Text = text
        self.Subject = subject
        self._to = cf.get("userInfo","to")
        self._from = cf.get("userInfo","from")
        self._pwd = cf.get("userInfo","pwd")
        self._send()

    def _send(self):
        msg = MIMEText(self.Text)
        msg['Subject'] = self.Subject
        msg['From'] = self._from
        msg['To'] = self._to
        try:
            server = smtplib.SMTP_SSL('smtp.qq.com',port=465)
            server.login(self._from,self._pwd)
            server.sendmail(self._from,self._to,msg.as_string())
            server.close()
            logger.info("send mail from %s to %s Text is %s Subject are %s" \
                        % (self._from,self._to,self.Text,self.Subject))
            logger.info("send mail right!")
        except Exception as e:
            logger.exception(e)

if __name__ == '__main__':
    sendmail("i love you", "I love you, love you")