#!user/bin/env python
#coding=utf-8

"""
Created on 2015/7/21
Author:LiQing
QQ:626924971
Tel:**********
Function:The base of tieba spider
"""

import random
import re
import urllib
import time
import requests

from get_conf import get_conf
from logger import logger

class spider(object):
    def __init__(self, timeout = int(get_conf.find(("image", ))["timeout"]), kwargs={}):
        self.http_header = get_conf.find(("http_header", "common"))
        self.http_header.update(kwargs)
        self.timeout = timeout


    def get_image_url_list(self, pattern, url):
        logger.info(url)
        time.sleep(int(get_conf.find(("image", ))["time_wait"]))
        try:
            http_response = requests.get(url, headers=self.http_header, timeout=self.timeout).content.decode('utf-8')
            return re.findall(pattern, http_response)
        except Exception as e:
            logger.error(e)
            return []

    def get_result(self, image_cnt, query, pattern):
        """
        @param image_cnt:需要的图片数量
        @param query:关键词
        @param pattern:抽取url的正则表达式
        """
        raise NotImplementedError()

class tieba_spider(spider):
    def __init__(self, timeout=int(get_conf.find(("image",))["timeout"])):
        kwargs = get_conf.find(("http_header", "baidu"))
        super(tieba_spider, self).__init__(timeout, kwargs)

    def get_result(self, image_cnt, query, pattern=r'"objURL":"(.*?)"'):
        result = []
        url =  get_conf.find(("url", "tieba"))["url"] % (
                urllib.quote(query), urllib.quote(query), 0, 30, random.randint(1000000, 9999999))
        for i in xrange(image_cnt / 50):
            if i == 0:
                url = get_conf.find(("url", "tieba"))["url"] % (
                urllib.quote(query), urllib.quote(query), 0, 30, random.randint(1000000, 9999999))
            elif i % 2:
                url = get_conf.find(("url", "baidu"))["url"] % (
                urllib.quote(query), urllib.quote(query), i * 30, i * 30, random.randint(1000000, 9999999))
            else:
                url = get_conf.find(("url", "baidu"))["url"] % (
                urllib.quote(query), urllib.quote(query), i * 30, (i - 1) * 30, random.randint(1000000, 9999999))
            result.extend(self.get_image_url_list(pattern, url))
        # logger.info(result)
        return result
