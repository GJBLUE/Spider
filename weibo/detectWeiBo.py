#coding:utf-8

from detect_manga import DetectManga
from datetime import datetime

import requests
import re
import conf

import sys
reload(sys)
sys.setdefaultencoding('utf8')

headers = conf.headers2

cookies = conf.cookies

class DetectWBNewManga:


    #获得需要的作者微博
    def getPage(self, url):
        response = requests.get(url, headers = headers, cookies = cookies, timeout = 4)
        page = response.content
        return page

    #暂时注释，如果现在用的cookies不是持久的
    #获得cookies，传入需要去获取的页面
    # def getPages(self, url):
    #     page = self.getPage(url)
    #     #出现这个found，就说明cookies过期了，我们需要重新获取cookies
    #     if 'found' in page:
    #         response = requests.get(conf.url, headers = conf.headers1)
    #         cookie = response.cookies
    #         r = requests.get(url, headers = headers2, cookies = cookie)
    #         pages = r.content
    #         return pages
    #     else:
    #         return page

   
    def getData(self):
        sql = "select * from new_weibo_table"
        cur = self.pool.execute(sql)
        l = []
        #输出格式，u'',
        for i in cur:
            l.append((i[0], i[1].encode('utf-8'), i[2].encode('utf-8')))
        return l

    def analyze(self):
        print "===================analyzing weibo======================="

        l = self.getData()
        cid = 0
        self.args = []
        for i in l:
            mid, target, url = i[0], i[1], i[2]
            uptime = str(datetime.now())
            page = self.getPage(url)
            #page = self.getPages(url)

            #获得微博标题和更新时间
            f = re.findall(r'\#%s\#.*?\>(.*?)\<.*?WB\_from.*?S\_txt2.*?title\=.*?\"(.*?)\".*?date'%(target), page)
            contents = []
            for i in f:
                time = i[1].replace('\\','')
                contents.append(time)

            #如果微博没有出现相关话题的跟新
            if contents == []:
                pass
            else:
                new_time = max(contents)
                mname = target
                cname = new_time
                curl = url + new_time
                print mname, cname, url, curl, uptime
                #self.args.append((mid, cid, target, new_time, url, url, uptime)) 
                self.handle_args(mname, cname, url, curl, uptime) 







