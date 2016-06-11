#!user/bin/env python
#coding=utf-8

"""
Created on 2015/6/11
Author:LiQing
QQ:626924971
Tel:**********
Function:The database manager
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DB_CONNECT_STRING = 'mysql+mysqldb://root:123456@localhost/?charset=utf8'
engine = create_engine(DB_CONNECT_STRING, echo=True)
DB_Session = sessionmaker(bind=engine)
session = DB_Session()

def _check_image_download_url():
    try:
        session.execute("create database if not exists image_download_url")
    except Exception as e:
        print e

if __name__ == "__main__":
    _check_image_download_url()