#!user/bin/env python
#coding=utf-8

"""
Created on 2015/7/21
Author:LiQing
QQ:626924971
Tel:**********
Function:The base of spider
"""

import random
import re
import urllib
import time
import requests

from get_conf import get_conf
from logger import logger
import baidu_translate_url

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

class baidu_spider(spider):
    def __init__(self, timeout=int(get_conf.find(("image", ))["timeout"])):
        kwargs = get_conf.find(("http_header", "baidu"))
        super(baidu_spider, self).__init__(timeout, kwargs)

    def get_result(self, image_cnt, query, pattern=r'"objURL":"(.*?)"'):
        result = []
        for i in xrange(image_cnt/30):
            if i == 0:
                url = get_conf.find(("url", "baidu"))["url"] % (urllib.quote(query),urllib.quote(query),0,30,random.randint(1000000,9999999))
            elif i % 2:
                url = get_conf.find(("url", "baidu"))["url"] % (urllib.quote(query),urllib.quote(query),i*30,i*30,random.randint(1000000,9999999))
            else:
                url = get_conf.find(("url", "baidu"))["url"] % (urllib.quote(query),urllib.quote(query),i*30,(i-1)*30,random.randint(1000000,9999999))
            result.extend(self.get_image_url_list(pattern ,url))
        #logger.info(result)
        return result

    def get_image_url_list(self, pattern, url):
        logger.info("[url]\t"+url)
        time.sleep(int(get_conf.find(("image", ))["time_wait"]))
        try:
            http_response = requests.get(url, headers=self.http_header, timeout=10)
            http_response_status = http_response.status_code
            http_response = http_response.content.decode('utf-8')
            try_cnt = 3
            while(http_response_status >= 300 and try_cnt > 0):
                time.sleep(int(get_conf.find(("image", ))["time_wait"]))
                http_response = requests.get(url, headers=self.http_header, timeout=10)
                http_response_status = http_response.status_code
                http_response = http_response.content.decode('utf-8')
                try_cnt -= 1
            if http_response_status >= 300:
                logger.warn(url)
            return [baidu_translate_url.decode(obj_url.encode("utf-8")) for obj_url in re.findall(pattern, http_response)]
        except Exception as e:
            logger.error(e)
            return []

class sougou_spider(spider):
    def __init__(self, timeout=int(get_conf.find(("image",))["timeout"])):
        kwargs = get_conf.find(("http_header", "sougou"))
        super(sougou_spider, self).__init__(timeout, kwargs)

    def get_result(self, image_cnt, query, pattern=r'"pic_url":"(.*?)"'):
        result = []
        for i in xrange(image_cnt / 48):
            url = get_conf.find(("url", "sougou"))["url"] % (
                urllib.quote(query), i*48)
            result.extend(self.get_image_url_list(pattern, url))
        # logger.info(result)
        return result

    def get_image_url_list(self, pattern, url):
        logger.info("[url]\t" + url)
        time.sleep(int(get_conf.find(("image",))["time_wait"]))
        try:
            http_response = requests.get(url, headers=self.http_header, timeout=10)
            http_response_status = http_response.status_code
            http_response = http_response.content
            try_cnt = 3
            while (http_response_status >= 300 and try_cnt > 0):
                time.sleep(int(get_conf.find(("image",))["time_wait"]))
                http_response = requests.get(url, headers=self.http_header, timeout=10)
                http_response_status = http_response.status_code
                http_response = http_response.content.decode('utf-8')
                try_cnt -= 1
            if http_response_status >= 300:
                logger.warn(url)
            return re.findall(pattern, http_response)
        except Exception as e:
            logger.error(e)
            return []

class qihu_spider(spider):
    """The spider is 360 spider, because name 360_spider is error name"""
    def __init__(self, timeout=int(get_conf.find(("image",))["timeout"])):
        kwargs = get_conf.find(("http_header", "360"))
        super(qihu_spider, self).__init__(timeout, kwargs)

    def get_result(self, image_cnt, query, pattern=r'"img":"(.*?)"'):
        result = []
        for i in xrange(image_cnt / 30):
            url = get_conf.find(("url", "360"))["url"] % (
                urllib.quote(query), i*30)
            result.extend(self.get_image_url_list(pattern, url))
        # logger.info(result)
        return result

    def get_image_url_list(self, pattern, url):
        logger.info("[url]\t" + url)
        time.sleep(int(get_conf.find(("image",))["time_wait"]))
        try:
            http_response = requests.get(url, headers=self.http_header, timeout=10)
            http_response_status = http_response.status_code
            http_response = http_response.content
            try_cnt = 3
            while (http_response_status >= 300 and try_cnt > 0):
                time.sleep(int(get_conf.find(("image",))["time_wait"]))
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

if __name__ == "__main__":
    # baiduSpider = baidu_spider()
    # urls = baiduSpider.get_result(1000, "dog")
    # sougouSpider = sougou_spider()
    # urls = sougouSpider.get_result(48, "狗")
    qihuSpider = qihu_spider()
    urls = qihuSpider.get_result(30, "dog")
    print(urls)