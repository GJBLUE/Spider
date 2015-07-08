#coding=utf-8

import urllib
import urllib2
import re
import json
import pdb
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

testUrl = 'www.baidu.com'

headers = {
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

#第一次请求的post
post1 ={
            'url':testUrl,
            'curl':'',
            'rt':'1',
            'nocache':'0',
            'host':'',
            'referer':'',
            'cookie':'',
            'agent':'',
            'speed':'',
            'verify':testUrl+'18371013654',
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

#获取POST后网页返回的数据
def getPage(url, post, headers):
    #获取request
    request = urllib2.Request(url, post, headers)
    #由于爬取17ce会出现httplib.BadStatusLine: ''错误，故抛出此错误。
    try:
        #打开网页
        response = urllib2.urlopen(request)
        page = response.read()
        data = eval(page)
        datas = json.dumps(data,ensure_ascii=False)

        jsondatas = json.loads(datas)
        return jsondatas
    except httplib.HTTPException, e:
        pass



#发送第一次POST所获得数据
def getFirstData():
    #POST地址
    targetUrl = 'http://www.17ce.com/site/http'
    post = urllib.urlencode(post1)
    
    #pdb.set_trace()
    #以dict形式获取到所需的数据
    data = getPage(targetUrl, post, headers)
    #print data['tid']
    return data['tid']

def getSecondData():
    #此处获得的是对应输入网址的post表单信息，获得对于该网址的关键
    tids = getFirstData()
    #第二个POST表单
    post2 = {
        'tid':tids,
        'num':'4',
        'ajax_over':'0'
    }
    post = urllib.urlencode(post2)
    #第二个POST网址
    targetUrl = 'http://www.17ce.com/site/ajaxfresh'
    #以dict形式获取到所需的数据
    datas = getPage(targetUrl, post, headers)
    data = datas['freshdata']
    #print data
    for key , value in data.items():
        print value['name'], value['speed']



if __name__ == '__main__':
    getSecondData()

    

