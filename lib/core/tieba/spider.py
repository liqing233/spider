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
    def __init__(self, timeout = int(get_conf.find(("tieba", ))["timeout"]), kwargs={}):
        self.http_header = get_conf.find(("http_header", "common"))
        self.http_header.update(kwargs)
        self.timeout = timeout


    def get_image_url_list(self, pattern, url):
        logger.info(url)
        time.sleep(int(get_conf.find(("tieba", ))["time_wait"]))
        try:
            http_response = requests.get(url, headers=self.http_header, timeout=self.timeout).content.decode('utf-8')
            return re.findall(pattern, http_response)
        except Exception as e:
            logger.error(e)
            return []

    def get_tieba_info_length(self, url, pattern):
        """
        @param url:第一个tieba页面的url，用来获取贴吧信息数目
        @param pattern:抽取url的正则表达式
        """
        raise NotImplementedError()

    def get_tieba_info(self, url, pattern):
        """
        @param url:tieba页面的url，用来获取贴吧一页中的信息
        @param pattern:抽取url的正则表达式
        """
        raise NotImplementedError()

    def get_result(self, query, pattern):
        """
        @param query:关键词
        @param pattern:抽取url的正则表达式
        """
        raise NotImplementedError()

class tieba_spider(spider):
    def __init__(self, timeout=int(get_conf.find(("tieba",))["timeout"])):
        kwargs = get_conf.find(("http_header", "baidu"))
        super(tieba_spider, self).__init__(timeout, kwargs)

    def get_result(self, query, pattern=r'"objURL":"(.*?)"'):
        result = []
        first_url = get_conf.find(("url", "tieba"))["url"] % (
            urllib.quote(query), 0)
        tieba_info_length = self.get_tieba_info_length(first_url, r'"<span class="red_text">(.*?)</span>篇"')
        logger.info(tieba_info_length)
        # for i in xrange(image_cnt / 50):
        #     url = get_conf.find(("url", "tieba"))["url"] % (
        #         urllib.quote(query), i*50)
        #     result.extend(self.get_image_url_list(pattern, url))
        # logger.info(result)
        return result

    def get_tieba_info(self, url, pattern):
        pass

    def get_tieba_info_length(self, url, pattern):
        logger.info("[url]\t" + url)
        time.sleep(int(get_conf.find(("tieba",))["time_wait"]))
        try:
            http_response = requests.get(url, headers=self.http_header, timeout=10)
            http_response_status = http_response.status_code
            http_response = http_response.content
            logger.info(http_response)
            try_cnt = 3
            while (http_response_status >= 300 and try_cnt > 0):
                time.sleep(int(get_conf.find(("tieba",))["time_wait"]))
                http_response = requests.get(url, headers=self.http_header, timeout=10)
                http_response_status = http_response.status_code
                http_response = http_response.content.decode('utf-8')
                try_cnt -= 1
            if http_response_status >= 300:
                logger.warn(url)
            return [obj_url.replace("\\", "") for obj_url in re.findall(pattern, http_response)]
        except Exception as e:
            logger.error(e)
            return []

    def get_image_url_list(self, pattern, url):
        logger.info("[url]\t" + url)
        time.sleep(int(get_conf.find(("tieba",))["time_wait"]))
        try:
            http_response = requests.get(url, headers=self.http_header, timeout=10)
            http_response_status = http_response.status_code
            http_response = http_response.content
            with open("http_response.txt", "w+") as f:
                f.write(http_response)
            try_cnt = 3
            null_flag = False
            while (http_response_status >= 300 and try_cnt > 0 and not null_flag):
                time.sleep(int(get_conf.find(("tieba",))["time_wait"]))
                http_response = requests.get(url, headers=self.http_header, timeout=10)
                http_response_status = http_response.status_code
                http_response = http_response.content.decode('utf-8')
                try_cnt -= 1
                if len(re.findall(pattern, http_response)) == 0:
                    null_flag = True
            if http_response_status >= 300:
                logger.warn(url)
            return [obj_url.replace("\\", "") for obj_url in re.findall(pattern, http_response)]
        except Exception as e:
            logger.error(e)
            return []

if __name__ == "__main__":
    # baiduSpider = baidu_spider()
    # urls = baiduSpider.get_result(1000, "dog")
    # sougouSpider = sougou_spider()
    # urls = sougouSpider.get_result(48, "狗")
    tiebaSpider = tieba_spider()
    urls = tiebaSpider.get_result("dog")
    print(urls)