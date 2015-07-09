#encoding=utf-8

import urllib
import urllib2
import os
import Queue
import threading
import cookielib
import httplib,re

#豆瓣小爬虫
class Spider():

	def __init__(self):
		self.loginURL="http://www.douban.com/"
		self.source='index_nav'
		self.form_email='895733091@qq.com'
		self.form_password='your passsword'
		self.post=post={
			'source':self.source,
			'form_email':self.form_email,
			'form_password':self.form_password
		}
		#对POST数据进行编码转换
		self.postData=urllib.urlencode(self.post)
		#设置cookie
		self.cookie=cookielib.LWPCookieJar()
		#设置cookie处理器
		self.cookieHandler=urllib2.HTTPCookieProcessor(self.cookie)
		#设置登录时用到的opener，他的open相当于urllib2.urlopen
		self.opener=urllib2.build_opener(self.cookieHandler,urllib2.HTTPHandler)

	#尝试登录
	def Login(self):
		#输入登陆所需信息
		request=urllib2.Request(self.loginURL,self.postData)
		#得到第一次登录的想应
		response=self.opener.open(request)
		#获取其中内容
		content=response.read()
		#获取状态吗
		status=response.getcode()
		#if status==302,success
		if status==200:
			print 'u are sucess'
		else:
			print 'u are fail'

	def getpage(self):
		try:
			url=self.loginURL
			request=urllib2.Request(url)
			response=urllib2.urlopen(request)
			#print response.read()
			return response
		except urllib2.URLError,e:
			if hasattr(e,"reason"):
				print u"爬取豆瓣失败，错误原因",e.reason
				return None



douban=Spider()
douban.Login()
douban.getpage()
