#!/usr/bin/env python
# coding=utf-8

import urllib
import urllib2
import cookielib
import httplib
import pdb
import json
import re
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

class ce:
    #初始化
    def __init__(self):
	#POST发送地址
	self.startUrl = 'http://www.17ce.com/site/ajaxfresh'
	#代理IP
	self.proxyURL = 'http://120.193.146.97:843'
	#headers信息
	self.headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.130 Safari/537.36',
            'Referer':'http://www.17ce.com/'
           # 'Origin':'http://www.17ce.com',
           # 'Content-type':'application/x-www-form-urlencoded',
           # 'Content-length':'223',
           # 'Host':'www.17ce.com',
           # 'Accept-Encoding':'gzip, deflate',
           # 'Connection':'keep-alive',
           # 'DNT':'1'
                }
		#POST数据
	self.post = urllib.urlencode({
            'tid':'201507_efe33f28599811a97e8de18bf2913df1',
            'num':'2',
            'ajax_over':'0'
		})


    #main
    def main(self):
        #将startUrl,postData,headers传入
        request = urllib2.Request(self.startUrl,self.post,self.headers)
        #发送请求
        try:
            #打开网页
            response = urllib2.urlopen(request)
         
    	    page = response.read()
            print type(page)
            # a = eval(page)
            # print a 
            # pattern = re.compile(r'\\|<.*?>', re.I|re.M|re.S)
            # filedata = pattern.sub('', page)
            # with open('c://Code/json.txt', 'w') as f:
            #     f.write(filedata)
                
            # with open('c://Code/json.txt', 'r') as f:
            #     # for line in f:
            #     #     print line
            #     d = f.read()
            #print type(d)
    	    # datas = json.dumps(page, ensure_ascii=False)

         #    jsondatas = json.loads(datas).encode('utf-8')
            data = eval(page)
            datas = json.dumps(data,ensure_ascii=False)
            print type(datas)
            jsondatas = json.loads(datas)
            #print jsondatas['freshdata']['2965']['name']
            data1 = jsondatas['freshdata']
    	    print type(data1)

                #mydict = eval(jsondatas)
                

    	except httplib.HTTPException, e:
    	    pass 
            


s = ce()
s.main()
