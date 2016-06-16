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
# engine = create_engine(DB_CONNECT_STRING, echo=True)
engine = create_engine(DB_CONNECT_STRING, echo=False)
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
        if len(table_exist) == 0 and table == "tieba_image_download":
            session.execute("CREATE TABLE  %s.%s(url varchar(512) NOT NULL PRIMARY KEY, " % (database, table) +
                            "download_status int(1), count int(10) default 1 )")
    except Exception as e:
        print e

def insert_table(database, table, data):
    if database == "tieba" and table == "tieba_image_download":
        if session.execute("select * from %s.%s where url = %s" % (database, table, data[0])):
            session.execute("insert into %s values('%s','%s', '%s')" % (table, data[0], int(data[1]), 1))
        else:
            if int(data[1]) and session.execute("select download_status from %s.%s where url = '%s'" % (database, table, data[0])):
                session.execute("update %s.%s set count = count + 1, download_status = 1 where url = %s" % (database, table, data[0]))
            else:
                session.execute("update %s.%s set count = count + 1, download_status = 0 where url = %s" % (database, table, data[0]))
    else:
        raise AttributeError("No database.table %s.%s" % (database, table))

def check_image_download_url(database, table, url):
    if session.execute("select * from %s.%s where url = '%s'" % (database, table, url)):
        return True
    else:
        return False


if __name__ == "__main__":
    check_table_exist(get_conf.find(("db", "table_info"))["database"], get_conf.find(("db", "table_info"))["table"])
    # _check_image_download_url()