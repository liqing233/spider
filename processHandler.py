#!/usr/bin/python
#coding=utf8

'''
Created on 2015/7/21
Author:LiQing
QQ:626924971
Tel:18674450812
Function:The main of Spider
'''

import os
import urllib
import re
from multiprocessing import Process, Queue, Lock
from collections import OrderedDict
import time
import configure
import baseSpider
import imageLoader
import set_demon

_global_lock = Lock()
_global_start_flag = False
_last_flag = False

class processDispatch(object):
    def __init__(self):
        self.imageLoader = imageLoader.imageLoader()
        self.query_max = set([query.strip() for query in open(configure.query_home, "r")])
        self.query_min = set([query.strip() for query in open(configure.finished_home, "r")])
        self.query_set = self.query_max - self.query_min
        self.url_queue = Queue()

    @staticmethod
    def instance():
        with _global_lock:
            if not hasattr(processDispatch, "_instance"):
                processDispatch._instance = processDispatch()
                return processDispatch._instance
            return processDispatch._instance

    def _queryProcessFunc(self):
        num = 0
        end_flag = False
	print "queryProcess"
        for query in self.query_set:
     	    print query
            if end_flag:
                break
            num += 1
	    print num
            urls = []
            if "baiduSipder" in configure.spider_source:
                urls.extend(baseSpider.baiduSipder(timeout=10).get_result(configure.image_cnt, urllib.quote(query)))
            if "googleSipder" in configure.spider_source:
               urls.extend(baseSpider.googleSipder(timeout=10).get_result(configure.image_cnt, urllib.quote(query)))
            if "yahooSipder" in configure.spider_source:
                urls.extend(baseSpider.yahooSipder(timeout=10).get_result(configure.image_cnt, urllib.quote(query)))
            if "beingSipder" in configure.spider_source:
                urls.extend(baseSpider.beingSipder(timeout=10).get_result(configure.image_cnt, urllib.quote(query)))
            if "flickrSipder" in configure.spider_source:
                urls.extend(baseSpider.flickrSipder(timeout=10).get_result(configure.image_cnt, urllib.quote(query)))
            
            if "twitterSpider" in configure.spider_source:
                urls.extend(baseSpider.twitterSpider(timeout=10).get_result(configure.image_cnt, urllib.quote(query)))
            else:
		print "falied"
 	    cnt = 0
            print("cnt of url is:"+str(len(urls)))
            dic = OrderedDict()
            for url in urls:
                #url = "".join([re.split("jpg|png|gif", url)[0], "jpg"])
                dic[url] = 0
            url_set = dic.keys()
            print("cnt of url set is:"+str(len(url_set)))
            for url in url_set:
                cnt += 1
                if cnt == len(url_set):
                    if num == len(self.query_set):
                        self.url_queue.put((query, url, cnt, -1))   #全体任务结束
                        end_flag = True
                        break
                    self.url_queue.put((query, url, cnt, 0))        #单个任务结束
                else:
                    self.url_queue.put((query, url, cnt, 1))        #普通任务

    def _imageProcessFunc(self):
        global _last_flag
        while True:
	   # print self.url_queue.qsize()
            url_info = self.url_queue.get()
            query = url_info[0]
            url = url_info[1]
            no = url_info[2]
            flag = url_info[3]
            image_type = "." + url.split(".")[-1]
            filepath = os.path.join(configure.image_path, query)
            filename = os.path.join(filepath, query+str(no)+image_type)
            self.imageLoader.down_load_image(filepath, filename, url, configure.try_cnt)
            if flag == 1:
                pass
            elif flag == 0:
                with _global_lock:
                    with open(configure.finished_home, "a+") as f:
                        f.write(query+"\n")
            else:
                self.url_queue.put(url_info)
                with _global_lock:
                    if not _last_flag:
                        _last_flag = True
                        with open(configure.finished_home, "a+") as f:
                            f.write(query+"\n")
                break

    def start(self):
        '''
        @brief:该方法只能调用一次,启动spider
        '''
        global _global_start_flag
        with _global_lock:
            if _global_start_flag:
                raise AttributeError("start() already started 该方法只能调用一次")
            _global_start_flag = True
        query_proc = Process(target=self._queryProcessFunc, args=())  
        query_proc.start()
        process_list = []
        for i in xrange(configure.imageLoader_process_cnt):
            child_proc = Process(target=self._imageProcessFunc, args=())  
            process_list.append(child_proc)
            child_proc.start()
        for proc in process_list:
            proc.join()
        query_proc.join()
        print("end with success")


if __name__ == "__main__":
#    set_demon.daemonize(stdout='../log/stdout.log', stderr='../log/stderr.log')
    a = time.time()
    processDispatch.instance().start()
    print time.time()-a




