#!/usr/bin/python
#coding=utf8

"""
Created on 2015/7/21
Author:LiQing
QQ:626924971
Tel:18674450812
Function:The process of Spider
"""

import os
import datetime
import logging
import logging.config
from multiprocessing import Pool, Process
import eventlet

from get_conf import get_conf
import image_download
import spider as sp

logging.config.fileConfig("../../../configures/log/logger.conf")
logger = logging.getLogger(__name__)

class process_handler(object):
    def __init__(self,spider):
        self.image_download = image_download.image_download()
        self.query_total = set([query.strip() for query in open(get_conf.find(("file", ))["query_home"], "r")])
        self.query_finished = set([query.strip() for query in open(get_conf.find(("file", ))["finished_home"], "r")])
        self.query_set = self.query_total - self.query_finished
        self.spider = spider
        self.query_process()

    def query_process(self):
        logger.info(self.spider)
        for query in self.query_set:
            logger.info("running"+query)
            urls = []
            if "baidu" == self.spider:
                baiduSpider = sp.baidu_spider()
                urls.extend(baiduSpider.get_result(int(get_conf.find(("image", ))["image_cnt"]), query))
            else:
                logger.error("no spider of"+query)
            logger.info("cnt of url is:"+str(len(urls)))
            imageDownload = []
            for cnt in range(len(urls)):
                imageDownload.append((query, query+str(cnt)+".jpg", urls[cnt], int(get_conf.find(("image", ))["try_cnt"])))
            green_pool = eventlet.GreenPool()
            green_pool.imap(self.image_download.down_load_image, imageDownload)

def query_process(pool):
    logger.info("spider process %s" % os.getpid())
    spiders = eval(get_conf.find(("image", ))["spider_source"])
    logger.info(spiders[0])
    for cnt in range(len(spiders)):
        pool.apply_async(process_handler, args=(spiders[cnt], ))
    pool.close()
    logger.info("All of spiders done")

def main():
    logger.info("start process")
    pool = Pool()
    pro = Process(target=query_process,args=(pool,))
    pro.start()
    pro.join()

if __name__ == "__main__":
    main()