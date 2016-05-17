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
    fp1 = open("test.txt","w+")
    fp1.write("task\t"+str(cnt))
    fp1.close()
    print("task\t"+str(cnt))
    print(datetime.datetime.now())

def event_process(cnt):
    print("event_process:\t"+str(cnt))
    print(datetime.datetime.now())
    green_pool = eventlet.GreenPool()
    green_pool.imap(task, cnt)

def query_process(pool):
    print 'Parent process %s.' % os.getpid()
    for cnt in range(5):
        pool.apply_async(event_process, args=(cnt,))
    print 'Waiting for all subprocesses done...'
    pool.close()
    #pool.join()
    print 'All subprocesses done.'

if __name__ == "__main__":
    print("start pool")
    pool = Pool()
    pro = Process(target=query_process,args=(pool,))
    pro.start()
    pro.join()
