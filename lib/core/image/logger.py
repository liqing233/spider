#!usr/bin/env python
#coding=utf8

"""
Created on 2015/7/21
Author:LiQing
QQ:626924971
Tel:*********
Function:The log configure of Spider
"""

import os
import logging

logger = logging.getLogger('spider')
logger.setLevel(logging.DEBUG)

logfile= r"../../../logs/spider.log"

if not os.path.exists(os.path.dirname(logfile)):
    try:
        os.makedirs(os.path.dirname(logfile))
    except Exception as e:
        print(e)

# 创建一个handler，用于写入日志文件
fh = logging.FileHandler(logfile)
fh.setLevel(logging.DEBUG)

# 再创建一个handler，用于输出到控制台
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# 定义handler的输出格式
formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s %(filename)s:%(lineno)s")
fh.setFormatter(formatter)
ch.setFormatter(formatter)

# 给logger添加handler
logger.addHandler(fh)
logger.addHandler(ch)