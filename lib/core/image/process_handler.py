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
from multiprocessing import Pool, Process,Queue, Lock, freeze_support
from collections import OrderedDict

from get_conf import get_conf
import image_download
import spider as sp
from logger import logger

global_lock = Lock()
global_start_flag = False

# def query_handler(spider, query_set):
#     logger.info("query_handler")
#     for query in query_set:
#         logger.info("[running]\t"+query)
#         if query != "":
#             urls = []
#             if "baidu" == spider:
#                 baiduSpider = sp.baidu_spider()
#                 urls.extend(baiduSpider.get_result(int(get_conf.find(("image", ))["image_cnt"]), query))
#             else:
#                 logger.error("No spider of\t"+query)
#                 raise AttributeError("No spider of\t"+query)
#             logger.info("[cnt]\tcnt of url is:"+str(len(urls)))
#             imageDownload = []
#             for cnt in range(len(urls)):
#                 imageDownload.append((query, query+str(cnt)+".jpg", urls[cnt], int(get_conf.find(("image", ))["try_cnt"])))
#             image_download_handler(imageDownload, query)
#
# def image_download_handler(imageDownload, query):
#     # green_pool = eventlet.GreenPool()
#     # for status in green_pool.imap(download.down_load_image, imageDownload):pass
#     # with open(get_conf.find(("file", ))["finished_home"], "a+") as f:
#     #     f.write(query+"\n")
#     download = image_download.image_download()
#     freeze_support()
#     try:
#         image_download_pool = Pool(processes=int(get_conf.find(("image", ))["download_image_process_cnt"]))
#         image_download_pool.map(download.down_load_image, imageDownload)
#         with open(get_conf.find(("file", ))["finished_home"], "a+") as f:
#             f.write(query+"\n")
#         image_download_pool.close()
#         image_download_pool.join()
#     except Exception as e:
#         logger.info(e)

class process_handler(object):
    def __init__(self):
        if os.path.exists(get_conf.find(("file", ))["query_home"]):
            query_total = set([query.strip() for query in open(get_conf.find(("file", ))["query_home"], "r")])
        else:
            raise AttributeError("No Exist %s" % get_conf.find(("file", ))["query_home"])
        query_finished = set()
        if os.path.exists(get_conf.find(("file", ))["finished_home"]):
            query_finished = set([query.strip() for query in open(get_conf.find(("file", ))["finished_home"], "r")])
        else:
            with open(get_conf.find(("file", ))["finished_home"], "w+"):pass
        self.query_set = list(query_total - query_finished)
        self.url_queue = Queue()
        self.download = image_download.image_download()
        self.spiders = eval(get_conf.find(("image", ))["spider_source"])

    @staticmethod
    def instance():
        with global_lock:
            if not hasattr(process_handler, "_instance"):
                process_handler._instance = process_handler()
                return process_handler._instance
            return process_handler._instance

    def query_handler(self):
        total_num = 0
        end_flag = False
        logger.info("query_handler")
        for query in self.query_set:
            if query != "":
                logger.info("query now is : %s" % query)
                if end_flag:
                    break
                total_num += 1
                logger.info("query num is : %s" % total_num)
                urls = []
                for spider in self.spiders:
                    logger.info(spider)
                    if "baidu" == spider:
                        baiduSpider = sp.baidu_spider()
                        urls.extend(baiduSpider.get_result(int(get_conf.find(("image", ))["image_cnt"]), query))
                    elif "sougou" == spider:
                        sougouSPider = sp.sougou_spider()
                        urls.extend(sougouSPider.get_result(int(get_conf.find(("image", ))["image_cnt"]), query))
                    elif "360" == spider:
                        qihuSpider = sp.qihu_spider()
                        urls.extend(qihuSpider.get_result(int(get_conf.find(("image",))["image_cnt"]), query))
                    else:
                        logger.error("No spider of\t"+spider)
                        raise AttributeError("No spider of\t"+spider)
                sigle_num = 0
                try:
                    logger.info("[cnt]\tcnt of url is:"+str(len(urls)))
                    dic = OrderedDict()
                    try:
                        for url in urls:
                            dic[url] = 0
                    except Exception as e:
                        logger.error(e)
                    url_set = dic.keys()
                    for url in url_set:
                        sigle_num += 1
                        if sigle_num == len(url_set):
                            if total_num == len(self.query_set):
                                self.url_queue.put((query, url, sigle_num, -1))   #全体任务结束
                                end_flag = True
                                break
                            self.url_queue.put((query, url, sigle_num, 0))        #单个任务结束
                        else:
                            self.url_queue.put((query, url, sigle_num, 1))        #普通任务
                except Exception as e:
                    logger.error(e)

    def image_download_handler(self):
        while True:
            #logger.info(self.url_queue.qsize())
            url_info = self.url_queue.get()
            query = url_info[0]
            url = url_info[1]
            order_number = url_info[2]
            flag = url_info[3]
            try:
                image_type = "." + url.split(".")[-1][:5]
                filename = query+str(order_number)+image_type
                self.download.down_load_image((query, filename, url, int(get_conf.find(("image", ))["try_cnt"])))
                if flag == 1:
                    pass
                elif flag == 0:
                    with global_lock:
                        with open(get_conf.find(("file", ))["finished_home"], "a+") as f:
                            f.write(query+"\n")
                else:
                    self.url_queue.put(url_info)
                    with global_lock:
                        with open(get_conf.find(("file", ))["finished_home"], "a+") as f:
                            fp1 = f.readlines()
                            if fp1[-1].strip() != query:
                                f.write(query + "\n")
                    break
            except Exception as e:
                logger.error(e)


    def start(self):
        global global_start_flag
        with global_lock:
            if global_start_flag:
                raise AttributeError("Spider already started !")
            global_start_flag = True
        logger.info("start process at %s" % str(datetime.datetime.now()))
        freeze_support()
        query_process = Process(target=self.query_handler, args=())
        query_process.start()
        image_download_process_list = []
        for cnt in xrange(int(get_conf.find(("image", ))["download_image_process_cnt"])):
            freeze_support()
            child_process = Process(target=self.image_download_handler, args=())
            image_download_process_list.append(child_process)
            child_process.start()
        for process in image_download_process_list:
            process.join()
        query_process.join()
        logger.info("end process at %s" % str(datetime.datetime.now()))

if __name__ == "__main__":
    process_handler.instance().start()