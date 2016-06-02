#!/usr/bin/env python
# coding=utf-8

import base64
import requests

from lxml import etree
from redisPool import RedisPool
from multiprocessing.dummy import Pool as ThreadPool
from settings import headers, payload, peuland, kxdaili, kuaidaili, xicidaili, peuHeaders


class NoneProxyException(Exception):
    pass


class Proxy(object):
    
    def __init__(self):
        self.db = RedisPool().conn()
        self.checked_proxy = []


    def addData(self):
        data = self.getPage(kxdaili)
        data.extend(self.getPage(kuaidaili))
        data.extend(self.getPage(xicidaili))
        data.extend(self.peuland_proxy())
        return data


    def check(self, proxy):
        
        try:
            page = requests.get('http://httpbin.org/ip', proxies=proxy, timeout=10)
            print page.status_code
            if page.status_code == 200:
                self.checked_proxy.append(proxy)
        except Exception as e:
            print e


    def getPage(self, info):

        url = info['url']
        num = info['page']
        proxies = []
        for i in range(num):
            i += 1
            urls = url.format(i)
            response = requests.get(urls, headers=headers, timeout=5)
            page = response.content
            tree = etree.HTML(page)
            ip = tree.xpath(info['urlxpath'])
            port = tree.xpath(info['portxpath'])
            ips = zip(ip, port)
            proxy = [{'http': "http://"+str(i[0])+":"+str(i[1])} for i in ips]
            proxies.extend(proxy)
        return proxies
    
    def saveData(self, data):
        self.db.hmset('url', data)


    def peuland_proxy(self):

        url = peuland['url']
        request = requests.Session()
        request.headers.update(peuHeaders)
        response = request.post(url, data=payload)
        datas = response.json()['data']
        proxy = []
        for line in datas:
            rate = int(base64.b64decode(line['time_downloadspeed']))
            if rate <= 7:
                continue
            proxy_type = base64.b64decode(line['type'])
            ip = base64.b64decode(line['ip'])
            port = base64.b64decode(line['port'])
            proxy.append({proxy_type: ip + ':' + port})
        return proxy

    
    
    def run(self):
        
        try: 
            proxy = self.addData()
        except Exception as e:
            raise NoneProxyException, 'data list is empty'
        pool = ThreadPool(8)
        pool.map(self.check, proxy)
        pool.close()
        pool.join()
        self.saveData(self.checked_proxy)
        print self.checked_proxy

if __name__ == '__main__':
    p = Proxy()
    p.run()

