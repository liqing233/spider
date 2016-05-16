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

logging.config.fileConfig("../../../configures/log/logger.conf")
logger = logging.getLogger(__name__)

class process_handler(object):
    def __init__(self):
        pass

def query_process(pool):
    logger.info("spider process %s" % os.getpid())
    #for cnt in range(5):
        #pool.apply_async(event_process, args=(cnt,))
    #print 'Waiting for all subprocesses done...'
    #pool.close()
    #print 'All subprocesses done.'

def main():
    logger.info("start process")
    pool = Pool()
    pro = Process(target=query_process,args=(pool,))
    pro.start()
    pro.join()

if __name__ == "__main__":
    main()