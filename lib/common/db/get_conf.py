#!user/bin/env python

"""
Created on 2015/6/15
Author:LiQing
QQ:626924971
Tel:*********
Function:get db conf
"""

import ConfigParser

class get_conf():
    @classmethod
    def find(cls, method):
        if method[0] == "db":
            db_manager = {}
            try:
                config = "../../../configures/db/db.conf"
                cf = ConfigParser.ConfigParser()
                cf.read(config)
                if method[1] == "db_login":
                    db_manager["user"] = cf.get("db_login", "user")
                    db_manager["password"] = cf.get("db_login", "password")
                    db_manager["location"] = cf.get("db_login", "location")
                elif method[1] == "table_info":
                    db_manager["database"] = cf.get("table_info", "database")
                    db_manager["table"] = cf.get("table_info", "table")
                else:
                    raise AttributeError("No Exist method of ('db_login', %s)" % method[1])
                return db_manager
            except Exception as e:
                print e

        else:
            raise AttributeError("No Exist method of %s" % method[0])

if __name__ == "__main__":
    print get_conf.find(("db", "table_info"))