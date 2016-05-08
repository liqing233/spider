#!user/bin/env python
#coding=utf8

'''
Created on 2015/7/21
Author:LiQing
QQ:626924971
Tel:18674450812
Function:The base of spider
'''

#import flickrapi
import random
import urllib2
import re
import urllib
import cookielib
import time
import json
#import lxml.html as HTML
#import lxml
import configure
from configure import image_size
from cookielib import CookieJar

class spider(object):
    def __init__(self, timeout=configure.timeout, kwargs={}):
        self.http_header = configure.http_header
        self.http_header.update(kwargs)
        self.timeout = timeout
        cookie_support = urllib2.HTTPCookieProcessor(cookielib.CookieJar())
        opener = urllib2.build_opener(cookie_support)  
        urllib2.install_opener(opener)

    def get_image_url_list(self, pattern, url):
        print(url)
        time.sleep(configure.time_wait)
        req = urllib2.Request(url, None, self.http_header)
        try:
            http_response = urllib2.urlopen(req, timeout=self.timeout).read()
            return re.findall(pattern, http_response)
        except Exception as e:
            print(e)
            return []

    def get_result(self, image_cnt, query, pattern):
        """
        @param image_cnt:需要的图片数量
        @param query:关键词
        @param pattern:抽取url的正则表达式
        """
        raise NotImplementedError()


class beingSipder(spider):
    def __init__(self, timeout=configure.timeout):
        kwargs = configure.being_header
        super(beingSipder, self).__init__(timeout, kwargs)

    def get_result(self, image_cnt, query, pattern="(?<=imgurl:&quot;)http:[^;]+?\.?(?:jpg|png)"):
        result = []
        i = 1
        while len(result) < image_cnt:
            if i == 1:
                url = "http://www.bing.com/images/search?q="+query
            else:
                url = "http://cn.bing.com/images/async?q="+query+"&async=content&first="+str(1+i*35)+"&count=35"
            result.extend(self.get_image_url_list(pattern, url))
            i += 1
        return result

    def get_image_url_list(self, pattern, url):
        print(url)
        time.sleep(configure.time_wait)
        try:
            cj = CookieJar()
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
            http_response = opener.open(url).read()
            return re.findall(pattern, http_response)
        except Exception as e:
            print(e) 
            return []

class yahooSipder(spider):
    def __init__(self, timeout=configure.timeout):
        kwargs = configure.yahoo_header
        super(yahooSipder, self).__init__(timeout, kwargs)

    def get_result(self, image_cnt, query, pattern="imgurl=(.*?)&rurl="):
        result = []
        for i in xrange(image_cnt/60+1):
            rand = str(time.time()).split(".")[0] + str(random.randint(100,999))
            b = i*60 + 1
            spos = i * 12
            url = "http://sg.images.search.yahoo.com/search/images?n=60&ei=UTF-8&fr=sfp&fr2=sa-gp-sg.images.search.yahoo.com&o=js\
&p=%s&tab=organic&tmpl=&nost=1&b=%s&iid=Y.%s&ig=6a0a89ab1b384c948100000000f3e811&spos=%s&&rand=%s"%(query, str(b), str(i), str(spos), rand)
            result.extend(self.get_image_url_list(pattern, url))
        return ["http://"+urllib.unquote(url) for url in result]


class baiduSipder(spider):
    def __init__(self, timeout=configure.timeout):
        kwargs = configure.baidu_header
        super(baiduSipder, self).__init__(timeout, kwargs)

    def get_result(self, image_cnt, query, pattern="objURL\":\"(http://.*?)\","):
        result = []
        for i in xrange(image_cnt/60+1):
            if configure.face == 1:
                url = "http://image.baidu.com/i?tn=baiduimagejson&word=%s&rn=60&pn=%d&face=1&ie=utf-8"%(query, i*60)
            else:
                url = "http://image.baidu.com/i?tn=baiduimagejson&word=%s&rn=60&pn=%d&ie=utf-8"%(query, i*60)
            result.extend(self.get_image_url_list(pattern, url))
        return result
class googleSipder(spider):
    def __init__(self, timeout=configure.timeout):
        kwargs = configure.google_header
        super(googleSipder, self).__init__(timeout, kwargs)

    def get_result(self, image_cnt, query, pattern="imgurl=(.*?)&amp;"):
        result = []
        for j in xrange(len(image_size)):
            for i in xrange(image_cnt/100+1):
                url ="https://www.google.com.hk/search?q=%s&safe=strict&hl=zh-CN&biw=1346&bih=624&site=webhp&tbs=isz:ex,iszw:%d,iszh:%d&tbm=isch&ijn=%d&ei=GT-SVfzQHcauogTGm5moCQ&start=%d" % (query,image_size[j][0],image_size[j][0],i,i*100)                
                result.extend(self.get_image_url_list(pattern, url))    

        return result
class flickrSipder(spider):
    def __init__(self, timeout=configure.timeout):
        kwargs = configure.flickr_header
        super(flickrSipder, self).__init__(timeout, kwargs)

    def get_result(self, image_cnt, query, pattern='url_.*?:"(.*?.jpg)'):
        result = []
        page = ""
        for i in xrange(1,45):
             url = "https://api.flickr.com/services/rest?sort=relevance&parse_tags=1&content_type=11&extras=can_comment,count_comments,count_faves,isfavorite,license,media,needs_interstitial,owner_name,path_alias,realname,rotation,url_c,url_l,url_m,url_n,url_q,url_s,url_sq,url_t,url_z&per_page=100&page=%d&lang=zh-Hant-HK&license=4,5,6,9,10&text=%s&method=flickr.photos.search&api_key=2291ba82f1bdd163733aae69399f709f&format=json&hermes=1&hermesClient=1&nojsoncallback=1" % (i,query)
             page,urlList = self.get_image_url_list(pattern,url)
             result.extend(urlList)    
        return result

    def get_image_url_list(self,pattern,url):
        print url
        time.sleep(configure.time_wait)
        flickr_date = urllib.urlencode(configure.flickr_date)
        req = urllib2.Request(url,flickr_date,self.http_header)
        try:
            http_response = urllib2.urlopen(req,timeout=self.timeout).read()
            info = json.loads(http_response)['photos']['photo']
            url_result = []
            for item in info:
                if item.has_key('url_z'):
                     new_url = item['url_z']
                elif item.has_key('url_m'):
	             new_url = item['url_m']
                if item.has_key('pathalias'):
                     new_path = item['pathalias']
                else:
                     new_path = 'other'
                url_result.append({new_url:new_path})
            return 1,url_result
        except Exception as e:
            print e,'#'
            return 1,[] 

class twitterSpider(spider):
    def __init__(self, timeout=configure.timeout):
        kwargs = configure.twitter_header
        super(twitterSpider, self).__init__(timeout, kwargs)

    def get_result(self, image_cnt, query, pattern=r"https:\/\/pbs.twimg.com\/media\/.+\.?(?:jpg|png)"):
        i = 1
        result = []
        count = 0

        # first url
        url = 'https://twitter.com/i/search/timeline?q=%s&src=typd&vertical=default&f=images&include_available_features=1&include_entities=1'%query
        print url
 
        # get image list from url response json
        response = urllib2.urlopen(url)
        data = json.load(response)
        html = data['items_html']
        imgs = set(re.findall(pattern, html))

        count += len(imgs)
        result.extend(imgs)

        # find second url in first url response json
        begin = html.rfind('data-tweet-id') + 15
        last = begin + 18
        nexturl = 'https://twitter.com/i/search/timeline?q=%s&src=typd&vertical=default&f=images&include_available_features=1&include_entities=1&max_position=TWEET-%s'%(query, html[begin:last])
        
        while count < image_cnt:
            time.sleep(configure.time_wait)
            response = urllib2.urlopen(nexturl)
            data = json.load(response)
            # find next url in current url response json
            nexturl = 'https://twitter.com/i/search/timeline?q=%s&src=typd&vertical=default&f=images&include_available_features=1&include_entities=1&max_position='%query + data['min_position']
            print nexturl
            # get image list from url response json
            html = data['items_html']
            imgs = set(re.findall(pattern, html))
            if len(imgs)==0:
                break
            count += len(imgs)
            result.extend(imgs)
        return result

def test():
    baidu = beingSipder()
    urls = baidu.get_result(1000, "hotdog")
    print urls,len(urls)

if __name__ == "__main__":
    test()


