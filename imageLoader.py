#!user/bin/env python
#coding=utf8

'''
Created on 2015/7/21
Author:LiQing
QQ:626924971
Tel:18674450812
Function:The Image download to filepath
'''

import urllib2
import os
from threading import Lock

import configure

_global_lock = Lock()

class imageLoader(object):
    def __init__(self):
        pass

    def down_load_image(self, filepath, filename, url, try_cnt):
        print(url)
        if try_cnt <= 0:
            with _global_lock:
                with open(configure.error_image_home, "a+") as f:
                    f.write(url+"\t"+filename+"\n")
            return
        try:
            filepath = filepath.decode("utf8").encode("gb2312")
            filename = filename.decode("utf8").encode("gb2312")
        except:
            return
        if not os.path.exists(filepath):
            try:
                os.makedirs(filepath)
            except:
                return
        req = urllib2.Request(url)
        req.add_header('User-agent', configure.user_agent_list[1])
        try:
            response = urllib2.urlopen(req, timeout=configure.timeout)
            res = response.read()
            if len(res) == 0:
                self.down_load_image(filepath, filename, url, try_cnt-1)
                return
            with open(filename, "wb") as jpg:
                jpg.write(res)
            print("download\t"+filepath)
        except Exception as e:
            self.down_load_image(filepath, filename, url, try_cnt-1)
            print("can't get image\t"+filepath)
            print(e)
            return




