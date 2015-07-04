#!/usr/bin/env python
# coding=utf-8


import urllib
import urllib2
import cookielib
import httplib

class ce:

	#初始化
	def __init__(self):
		#POST发送地址
		self.startUrl = 'http://www.17ce.com/site/http'
		#代理IP
		self.proxyURL = 'http://120.193.146.97:843'
		#headers信息
		self.headers = {
			'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.130 Safari/537.36',
            'Referer':'www.17ce.com',
            'Proxy-Connection':'keep-alive',
            'Origin':'http://www.17ce.com',
            'Content-type':'application/x-www-form-urlencoded',
            'Content-length':'223',
            'Host':'www.17ce.com',
            'Accept-Encoding':'gzip, deflate, sdch',
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Connection':'keep-alive',
            'DNT':'1',
            'Cookie':'maxid=35415; PHPSESSID=4vo49788584nukp9f0675jka77; __utmt=1; __utma=45994468.1573840565.1435998656.1435998656.1435998656.1; __utmb=45994468.1.10.1435998656; __utmc=45994468; __utmz=45994468.1435998656.1.1.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; allSites=www.baidu.com'
                }
		#POST数据
		self.post = post = {
			'url':'www.baidu.com',
    		'curl':'',
    		'rt':'1',
    		'nocache':'0',
    		'host':'',
    		'referer':'',
    		'cookie':'',
    		'agent':'',
    		'speed':'',
    		'verify':'www.baidu.com18371013654',
    		'pingcount':'',
    		'pingsize':'',
    		'area[]':'0',
    		'area[]':'1',
    		'area[]':'2',
    		'area[]':'3',

    		'isp[]':'0',
    		'isp[]':'1',
    		'isp[]':'2',
    		'isp[]':'6',
    		'isp[]':'7',
    		'isp[]':'8',
    		'isp[]':'4'
		}
		#将POST数据进行编码转换
		self.postData = urllib.urlencode(self.post)
		#设置代理
		self.proxy = urllib2.ProxyHandler({'http':self.proxyURL})
		#设置cookie
		self.cookie = cookielib.LWPCookieJar()
		#设置cookie处理器
		self.cookieHandler = urllib2.HTTPCookieProcessor(self.cookie)
		#打开网页用到的opener，它的open == urllib2.urlopen
		self.opener = urllib2.build_opener(self.cookieHandler, self.proxy, urllib2.HTTPHandler)

	#main
	def main(self):
            
	    #将startUrl,postData,headers传入
            request = urllib2.Request(self.startUrl,self.postData,self.headers)
	    #发送请求
	    #response = self.opener.open(request)
            print '@'*10
            try:
                #打开网页
            	response = urllib2.urlopen(request)
                print type(response)
            	#获取内容
    	    	page = response.read()
                print 123
    	    	print '#'*10+page
            except httplib.HTTPException, e:
	        pass 
	    
	   

s = ce()
s.main()
