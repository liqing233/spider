#!user/bin/env python
#coding=utf-8

"""
Created on 2015/7/21
Author:LiQing
QQ:626924971
Tel:*********
Function:translate baidu image url to right url
"""

from string import maketrans

def decode(url):
    str_table = {
    '_z2C$q': ':',
    '_z&e3B': '.',
    'AzdH3F': '/'
    }
    input_table = "wkv1ju2it3hs4g5rq6fp7eo8dn9cm0bla"
    output_table = "abcdefghijklmnopqrstuvw1234567890"
    tran_table = maketrans(input_table, output_table)
    for key, value in str_table.items():
        url = url.replace(key, value)

    return url.translate(tran_table)