#!/usr/bin/python
#coding=utf8

"""
Created on 2015/7/21
Author:LiQing
QQ:626924971
Tel:18674450812
Function:The process of Spider
"""

from multiprocessing import Pool, Process
import eventlet
import os, datetime

def task(cnt):
    print("task\t"+str(cnt))
    #print(datetime.datetime.now())
    return cnt, datetime.datetime.now()

def event_process(cnt):
    print("event_process:\t"+str(cnt))
    print(datetime.datetime.now())
    green_pool = eventlet.GreenPool()
    for cnt, Time in  green_pool.imap(task, [1,2,3,4,5]):
        #print(str(cnt))
        #print(Time)
        pass

def query_process():
    print 'Parent process %s.' % os.getpid()
    pool = Pool(5)
    for cnt in range(5):
        pool.apply_async(event_process, args=(cnt,))
    print 'Waiting for all subprocesses done...'
    pool.close()
    #pool.join()
    print 'All subprocesses done.'


if __name__ == "__main__":
    print("start pool")
    #event_process(5)
    #pool = Pool()
    pro = Process(target=query_process,args=())
    #pro = Process(target=event_process,args=(5,))
    pro.start()
    pro.join()
