#!user/bin/env python
#encoding=utf8

"""
Created on 2015/7/21
Author:LiQing
QQ:626924971
Tel:*********
Function:login in Baidu Tieba
"""

import time
import re
import rsa
import random
import math
import base64
import cookielib
import urllib
import urllib2
import requests

from get_conf import get_conf
from logger import logger

class login(object):
    def __init__(self, timeout = int(get_conf.find(("tieba", ))["timeout"]), kwargs={}):
        self.http_header = get_conf.find(("http_header", "common"))
        self.http_header.update(kwargs)
        self.timeout = timeout

    def login(self, pattern, url):
        logger.info(url)
        time.sleep(int(get_conf.find(("tieba", ))["time_wait"]))
        try:
            http_response = requests.get(url, headers=self.http_header, timeout=self.timeout).content.decode('utf-8')
            return re.findall(pattern, http_response)
        except Exception as e:
            logger.error(e)
            return []

    def check(self, pattern, url):
        """
        @param url:登录检测URL
        @param pattern:抽取url的正则表达式
        """
        raise NotImplementedError()

class tieba_login(login):
    def __init__(self, timeout=int(get_conf.find(("tieba", ))["timeout"])):
        kwargs = get_conf.find(("http_header", "baidu_login"))
        super(tieba_login, self).__init__(timeout, kwargs)

    def login(self, pattern = u'"token" : "(?P<tokenVal>.*?)"', url = get_conf.find(("login", "tieba"))["url"]):
        global cj
        cj = cookielib.CookieJar()

        logger.info(self.http_header)
        logger.info(url)

        token, init_time = self.get_token(url)
        login_time = str(int(time.time() * 1000))
        gid = self.get_gid()
        session = requests.session()
        callback = self.get_callback()
        pubkey, key = self.get_publickey(token=token, session=session, publickey_callback=callback, gid=gid)

        login_postdata = get_conf.find(("login", "baidu_login"))
        login_postdata["token"] = token
        login_postdata["tt"] = login_time
        login_postdata["gid"] = gid
        login_postdata["rsakey"] = key
        login_postdata["password"] = self.get_password(login_postdata["password"], pubkey)
        login_postdata["ppui_logintime"] = str(int(login_time) - int(init_time))
        login_postdata["callback"] = callback
        logger.info(login_postdata)

        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        urllib2.install_opener(opener)
        req = urllib2.Request(get_conf.find(("login", "tieba"))["login"], urllib.urlencode(login_postdata), self.http_header)
        http_response = urllib2.urlopen(req,timeout=self.timeout)
        logger.info(http_response)

        self.check(r'"user_name_show":"(.*?)"', get_conf.find(("login", "tieba"))["check"])

    @staticmethod
    def get_token(url):
        global cj
        init_time = str(int(time.time() * 1000))
        try:
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
            urllib2.install_opener(opener)
            # Debug the error "the fisrt two args should be string type:0,1!" must have the last sentence
            urllib2.urlopen(get_conf.find(("login", "tieba"))["home"])
            #获取token
            token = urllib2.urlopen(url).read()
            try:
                token=token.decode('utf-8')
            except:
                token=token.decode('gbk','ignore')
            finally:
                match = re.search(u'"token" : "(?P<tokenVal>.*?)"',token)
                token_val = match.group('tokenVal')
                logger.info(token_val)
                return token_val, init_time
        except Exception as e:
            logger.error(e)
            return "", init_time

    # 同一个登录下 token 是唯一的
    @staticmethod
    def get_token_requests(token_callback, gid, session, headers):
        # 此处必须是自己构造 url 不能采用 params 的参数， params 参数的顺序是变化的
        init_time = str(int(time.time() * 1000))
        token_url = "https://passport.baidu.com/v2/api/?getapi&tpl=pp&apiver=v3&tt="
        token_url = token_url + init_time + "&class=login&gid="
        token_url = token_url + gid + "&logintype=basicLogin&callback="
        token_url = token_url + token_callback

        token_html = session.get(token_url, headers=headers)
        token_content_all = token_html.text.replace(token_callback, "")
        token_content_all = eval(token_content_all)

        return token_content_all['data']['token'], init_time

    # gid 在同一个登录的 session 相同
    @staticmethod
    def get_gid():
        gid = "xxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx"
        gid = list(gid)
        for xy in range(len(gid)):
            if gid[xy] in "xy":
                r = int(random.random()*16)
                if gid[xy] == "x":
                    gid[xy] = hex(r).replace("0x", '').upper()
                else:
                    gid[xy] = hex(r & 3 | 8).replace("0x", '').upper()
            else:
                pass
        return ''.join(gid)

    # 每次都不同
    @staticmethod
    def get_callback():
        loop = '0123456789abcdefghijklmnopqrstuvwxyz'
        prefix = "bd__cbs__"
        n = math.floor(random.random() * 2147483648)
        a = []
        while n != 0:
            a.append(loop[int(n) % 36])
            n = n // 36
        a.reverse()
        callback = prefix + ''.join(a)
        return callback

    @staticmethod
    def get_publickey(token, session, publickey_callback, gid):
        publickey_url = "https://passport.baidu.com/v2/getpublickey?token="
        publickey_url = publickey_url + token + "&tpl=pp&apiver=v3&tt="
        publickey_url = publickey_url + str(int(time.time() * 1000)) + "&gid="
        publickey_url = publickey_url + gid + "&callback="
        publickey_url = publickey_url + publickey_callback

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
            "Host": "passport.baidu.com",
            "Referer": "https://passport.baidu.com/v2/?login"
        }
        publickey_html = session.get(publickey_url, headers=headers)
        publickey_content_all = eval(publickey_html.text.replace(publickey_callback, ""))

        return publickey_content_all['pubkey'], publickey_content_all['key']

    # 密码加密
    @staticmethod
    def get_password(password, pubkey):
        pub = rsa.PublicKey.load_pkcs1_openssl_pem(pubkey.encode("utf-8"))
        password_input = password.encode("utf-8")
        psword = rsa.encrypt(password_input, pub)
        psword = base64.b64encode(psword)
        return psword.decode("utf-8")

    def check(self, pattern, url):
        global cj
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        urllib2.install_opener(opener)

        content = urllib2.urlopen(url).read()
        content = content.decode('gbk').encode('utf8')
        if re.findall(pattern, content)[0] == get_conf.find(("login", "login_check"))["name"]:
            cookie = ""
            for item in cj:
                cookie += item.name+"="+item.value+";"
            cookie = cookie.rstrip(";")
            return cookie
        else:
            return ""

if __name__ == "__main__":
    tiebaLogin = tieba_login()
    tiebaLogin.login()
