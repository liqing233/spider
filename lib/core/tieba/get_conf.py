#!user/bin/env python

"""
Created on 2015/6/3
Author:LiQing
QQ:626924971
Tel:*********
Function:get spider conf
"""

import os
import ConfigParser
import xml.dom.minidom

from logger import logger

class get_conf():
    @classmethod
    def find(cls, method):
        if method[0] == "http_header":
            header = {}
            try:
                DOMTree = xml.dom.minidom.parse("../../../configures/http_header/http_header.xml")
                Data = DOMTree.documentElement
                http_headers = Data.getElementsByTagName("tieba")
                if method[1] == "baidu":
                    for http_header in http_headers:
                        if http_header.getAttribute("name") == "baidu":
                            header["Accept"] = http_header.getElementsByTagName('Accept')[0].childNodes[0].data.encode("utf-8")
                            header["Accept-Language"] = http_header.getElementsByTagName('Accept-Language')[0].childNodes[0].data.encode("utf-8")
                            header["Host"] = http_header.getElementsByTagName('Host')[0].childNodes[0].data.encode("utf-8")
                            header["Referer"] = http_header.getElementsByTagName('Referer')[0].childNodes[0].data.encode("utf-8")
                            header["User-Agent"] = http_header.getElementsByTagName('User-Agent')[0].childNodes[0].data.encode("utf-8")
                            #header["Cookie"] = http_header.getElementsByTagName('Cookie')[0].childNodes[0].data.encode("utf-8")
                elif method[1] == "common":
                    for http_header in http_headers:
                        if http_header.getAttribute("name") == "common":
                            header["Accept"] = http_header.getElementsByTagName('Accept')[0].childNodes[0].data.encode("utf-8")
                            header["Accept-Encoding"] = http_header.getElementsByTagName('Accept-Encoding')[0].childNodes[0].data.encode("utf-8")
                            header["Accept-Language"] = http_header.getElementsByTagName('Accept-Language')[0].childNodes[0].data.encode("utf-8")
                            header["Connection"] = http_header.getElementsByTagName('Connection')[0].childNodes[0].data.encode("utf-8")
                            header["User-Agent"] = http_header.getElementsByTagName('User-Agent')[0].childNodes[0].data.encode("utf-8")
                return header
            except Exception as e:
                logger.error(e)
        elif method[0] == "tieba":
            tieba = {}
            try:
                config = "../../../configures/tieba_conf/tieba.conf"
                cf = ConfigParser.ConfigParser()
                cf.read(config)
                tieba["timeout"] = cf.get("spider", "timeout")
                tieba["time_wait"] = cf.get("spider", "time_wait")
                tieba["try_cnt"] = cf.get("spider", "try_cnt")
                tieba["download_image_process_cnt"] = cf.get("spider", "download_image_process_cnt")
                tieba["query_type"] = cf.get("spider", "query_type")
                return tieba
            except Exception as e:
                logger.error(e)
        elif method[0] == "url":
            url = {}
            try:
                config = "../../../configures/tieba_conf/tieba.conf"
                cf = ConfigParser.ConfigParser()
                cf.read(config)
                if method[1] == "tieba":
                    url["url"] = cf.get("tieba", "url")
                return url
            except Exception as e:
                logger.error(e)
        elif method[0] == "file":
            file_home = {}
            try:
                config = "../../../configures/tieba_conf/tieba.conf"
                cf = ConfigParser.ConfigParser()
                cf.read(config)
                conf_path_abspath = os.path.join(os.getcwd(), config)
                file_home["image_path"] = os.path.join(os.path.dirname(conf_path_abspath), cf.get("file_home", "image_path"))
                file_home["query_home"] = os.path.join(os.path.dirname(conf_path_abspath), cf.get("file_home", "query_home"))
                file_home["finished_home"] = os.path.join(os.path.dirname(conf_path_abspath), cf.get("file_home", "finished_home"))
                file_home["error_home"] = os.path.join(os.path.dirname(conf_path_abspath), cf.get("file_home", "error_home"))
                file_home["download_record_home"] = os.path.join(os.path.dirname(conf_path_abspath), cf.get("file_home", "download_record_home"))
                return file_home
            except Exception as e:
                logger.error(e)

        else:
            raise NoMethod(method)

def NoMethod(method):
    logger.error("[find]get_conf::find Not have %s method" % str(method))

if __name__ == "__main__":
    get_conf.find(("file", ))