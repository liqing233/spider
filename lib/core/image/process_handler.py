#!/usr/bin/python
#coding=utf8

"""
Created on 2015/7/21
Author:LiQing
QQ:626924971
Tel:*********
Function:The process of Spider
"""

import os
import datetime
from multiprocessing import Process
import eventlet

from get_conf import get_conf
import image_download
import spider as sp

from logger import logger

def process_handler(spider):
    logger.info("start process_handler\t"+spider)
    download = image_download.image_download()
    if os.path.exists(get_conf.find(("file", ))["query_home"]):
        query_total = set([query.strip() for query in open(get_conf.find(("file", ))["query_home"], "r")])
    else:
        raise AttributeError("No Exist %s" % get_conf.find(("file", ))["query_home"])
    query_finished = set()
    if os.path.exists(get_conf.find(("file", ))["finished_home"]):
        query_finished = set([query.strip() for query in open(get_conf.find(("file", ))["finished_home"], "r")])
    else:
        with open(get_conf.find(("file", ))["finished_home"], "w+"):pass
    query_set = list(query_total - query_finished)
    logger.info(query_set)
    for query in query_set:
        #print(query)
        logger.info("[running]\t"+query)
        if query != "":
            try:
                urls = []
                if "baidu" == spider:
                    baiduSpider = sp.baidu_spider()
                    urls.extend(baiduSpider.get_result(int(get_conf.find(("image", ))["image_cnt"]), query))
                else:
                    logger.error("no spider of"+query)
                logger.info("[cnt]\tcnt of url is:"+str(len(urls)))
                imageDownload = []
                for cnt in range(len(urls)):
                    imageDownload.append((query, query+str(cnt)+".jpg", urls[cnt], int(get_conf.find(("image", ))["try_cnt"])))
                green_pool = eventlet.GreenPool()
                for status in green_pool.imap(download.down_load_image, imageDownload):pass
                with open(get_conf.find(("file", ))["finished_home"], "a+") as f:
                    f.write(query+"\n")
            except Exception as e:
                logger.error(e)

# def query_process():
#     logger.info("spider process %s" % os.getpid())
#     spiders = eval(get_conf.find(("image", ))["spider_source"])
#     logger.info(spiders[0])
#     pool = Pool(len(spiders))
#     for cnt in range(len(spiders)):
#         pool.apply_async(process_handler, args=(spiders[cnt], ))
#     pool.close()
#     logger.info("All of spiders done")

def main():
    logger.info("start process at %s" % str(datetime.datetime.now()))
    spiders = eval(get_conf.find(("image", ))["spider_source"])
    for cnt in range(len(spiders)):
        pro = Process(target=process_handler, args=(spiders[cnt], ))
        pro.start()
        logger.info("spider process is %s" % pro.pid)
    logger.info("end process at %s" % str(datetime.datetime.now()))

if __name__ == "__main__":
    main()