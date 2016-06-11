#!user/bin/env python
#encoding=utf8

"""
Created on 2015/7/21
Author:LiQing
QQ:626924971
Tel:*********
Function:login in Baidu Tieba
"""

import urllib2
import urllib
import cookielib
import re
from httplib import HTTPConnection
import gzip
import bs4
import json

URL_BAIDU_INDEX = u'http://www.baidu.com/'
#URL_BAIDU_INDEX = u'https://passport.baidu.com/v2/api/?getapi&tpl=mn&class=login'
URL_BAIDU_TOKEN = 'https://passport.baidu.com/v2/api/?getapi&tpl=pp&apiver=v3&class=login'
URL_BAIDU_LOGIN = 'https://passport.baidu.com/v2/api/?login'

#设置用户名、密码
username = '626929024@qq.com'
password = 'liq1988127'

#设置cookie，这里cookiejar可自动管理，无需手动指定
cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
urllib2.install_opener(opener)
reqReturn = urllib2.urlopen(URL_BAIDU_INDEX)

#获取token,
tokenReturn = urllib2.urlopen(URL_BAIDU_TOKEN).read()
try:
    tokenReturn=tokenReturn.decode('utf-8')
except:
    tokenReturn=tokenReturn.decode('gbk','ignore')

Cs = ""
for item in cj:
    Cs += item.name+"="+item.value+";"
print(Cs)

pattern=u'"token" : "(.*?)"'
match = re.findall(pattern, tokenReturn)
print(type(match[0]))
matchVal = re.search(u'"token" : "(?P<tokenVal>.*?)"',tokenReturn)
print(matchVal)
tokenVal = matchVal.group('tokenVal')
print(tokenVal)

#构造登录请求参数，该请求数据是通过抓包获得，对应https://passport.baidu.com/v2/api/?login请求
postData = {
    'username' : username,
    'password' : password,
    'u' : 'https://passport.baidu.com/',
    'tpl' : 'pp',
    'token' : tokenVal,
    'staticpage' : 'https://passport.baidu.com/static/passpc-account/html/v3Jump.html',
    'isPhone' : 'false',
    'charset' : 'UTF-8',
    'callback' : 'parent.bd__pcbs__ra48vi'
    }
postData = urllib.urlencode(postData)

#发送登录请求
loginRequest = urllib2.Request(URL_BAIDU_LOGIN,postData)
loginRequest.add_header('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
loginRequest.add_header('Accept-Encoding','gzip,deflate,sdch')
loginRequest.add_header('Accept-Language','zh-CN,zh;q=0.8')
loginRequest.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.36');
loginRequest.add_header('Content-Type','application/x-www-form-urlencoded')
sendPost = urllib2.urlopen(loginRequest).read()
try:
    sendPost=sendPost.decode('utf-8')
except:
    sendPost=sendPost.decode('gbk','ignore')

print(sendPost)

#查看贴吧个人主页 ，测试是否登陆成功，由于cookie自动管理，这里处理起来方便很多
#http://tieba.baidu.com/home/main?un=XXXX&fr=index 这个是贴吧个人主页，各项信息都可以在此找到链接
#teibaUrl = 'http://tieba.baidu.com/f/like/mylike?v=1387441831248'
# headers = dict()
# headers["Connection"] = "keep-alive"
# headers["Cache-Control"] = "max-age=0"
# headers["Accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
# headers["User-Agent"] = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.107 Safari/537.36"
# headers["Content-Type"] = "application/x-www-form-urlencoded"
# headers["Accept-Encoding"] = "gzip,deflate,sdch"
# headers["Accept-Language"] = "zh-CN,zh;q=0.8"
# conn = HTTPConnection("tieba.baidu.com", 80)
# conn.request("GET", "/f/user/json_userinfo", "", headers)
# resp = conn.getresponse()
# data = gzip.decompress(resp.read()).decode("GBK")
# print(data)


teibaUrl="http://tieba.baidu.com/f/user/json_userinfo"
content = urllib2.urlopen(teibaUrl).read()
content = content.decode('gbk').encode('utf8')
print content
#解析数据，用的BeautifulSoup4，感觉没有jsoup用的爽
# soup = bs4.BeautifulSoup(content)
# list = soup.findAll('tr')
# list = list[1:len(list)]
# careTeibalist = []
# print '贴吧链接\t吧名\t等级'
# for elem in list:
#     soup1 = bs4.BeautifulSoup(str(elem))
#     print 'http://tieba.baidu.com/'+soup1.find('a')['href']+'\t'+soup1.find('a')['title']+'\t'+soup1.find('a',{'class','like_badge'})['title']