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

from get_conf import get_conf

db_login = get_conf.find(("db", "db_login"))
DB_CONNECT_STRING = 'mysql+mysqldb://%s:%s@%s/?charset=utf8' % \
                    (db_login["user"], db_login["password"], db_login["location"])
engine = create_engine(DB_CONNECT_STRING, echo=True)
DB_Session = sessionmaker(bind=engine)
session = DB_Session()

def check_table_exist(database, table):
    try:
        session.execute("create database if not exists %s " % database)
        session.execute("use %s " % database)
        table_exist = session.execute("select * from information_schema.TABLES " +
                                      "where table_schema='%s' and table_name='%s'"
                                      % (database, table)).fetchall()
        # table not exist
        if len(table_exist) == 0:
            session.execute("CREATE TABLE  %s.%s(url varchar(512) NOT NULL PRIMARY KEY, " % (database, table) +
                            "download_status int(1), count int(10) default 1 )")
    except Exception as e:
        print e

def check_image_download_url():
    try:
        session.execute("create database if not exists image_download_url")
    except Exception as e:
        print e

if __name__ == "__main__":
    check_table_exist(get_conf.find(("db", "table_info"))["database"], get_conf.find(("db", "table_info"))["table"])
    # _check_image_download_url()