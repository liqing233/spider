#!user/bin/env python
#coding=utf8

"""
Created on 2015/7/21
Author:LiQing
QQ:626924971
Tel:*********
Function:The Image download to filepath
"""

import os
import datetime
import urllib2
from threading import Lock

from get_conf import get_conf
from logger import logger

_global_lock = Lock()

class image_download(object):
    def __init__(self):
        pass

    def down_load_image(self, image):
        file_path = image[0]
        file_name = image[1]
        url = image[2]
        try_cnt = image[3]

        if try_cnt <= 0:
            with _global_lock:
                with open(get_conf.find(("file", ))["error_home"], "a+") as f:
                    f.write(str(datetime.datetime.now())+"\t"+url+"\t"+os.path.join(file_path, file_name)+"\n")
            return False
        # try:
        #     file_path = file_path.decode("utf8").encode("gb2312")
        #     file_name = file_name.decode("utf8").encode("gb2312")
        # except:
        #     return False
        if not os.path.exists(os.path.join(get_conf.find(("file", ))["image_path"], file_path)):
            try:
                os.makedirs(os.path.join(get_conf.find(("file", ))["image_path"], file_path))
            except:
                return False
        req = urllib2.Request(url)
        req.add_header('User-agent', get_conf.find(("http_header", "common"))["User-Agent"])
        try:
            response = urllib2.urlopen(req, timeout = int(get_conf.find(("image", ))["timeout"]))
            res = response.read()
            if len(res) == 0:
                self.down_load_image((file_path, file_name, url, try_cnt-1))

            with open(os.path.join(get_conf.find(("file", ))["image_path"], file_path, file_name), "wb") as jpg:
                jpg.write(res)
                with open(get_conf.find(("file", ))["download_record_home"], "a+") as f:
                    f.write(str(datetime.datetime.now())+"\t"+"[download]"+"\t"+url+"\t"+os.path.join(file_path, file_name)+"\n")
                    logger.info("[download]\t"+os.path.join(file_path, file_name))
            return True

        except Exception as e:
            self.down_load_image((file_path, file_name, url, try_cnt-1))
            logger.error("can't get image\t"+os.path.join(get_conf.find(("file", ))["image_path"], file_path, file_name))
            logger.error(e)
            return False

if __name__ == "__main__":
    image_download = image_download()
    Image = ("dog", "dog1.jpg", "http://i1.s.hjfile.cn/entry/201310/b6b686d9-83d5-4efb-ab24-7b754342ba9b.jpg", 3)
    image_download.down_load_image(Image)
