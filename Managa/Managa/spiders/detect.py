#!/usr/bin/env python
# coding=utf-8

from scrapy.spider import Spider, Request
from scrapy.selector import Selector
from Managa.items import ManagaItem
from Managa import pipelines

import base64
import re


class u17Spider(Spider):

    name = "u17"
    allowed_domains = ["u17.com"]
    download_delay = 0.5
    
    pipeline = set([
        pipelines.u17Pipeline,
    ])

    start_urls = [
        "http://www.u17.com/comic/190.html",
        "http://www.u17.com/comic/195.html"
    ]
    
    def __init__(self):
        self.item = ManagaItem()

    def parse(self, response):
        '''get new chapter'''
        sel = Selector(response)
        sites = sel.xpath('//*[@id="chapter"]/li')

        
        cname = sites.xpath('a/@title').extract()[-2:]
        curl = sites.xpath('a/@href').extract()[-2:]
        cvip = sites.xpath('a/@class').extract()[-2:]
        
        if cvip[-1] == 'vip_chapter':
            self.item["cname"] = cname[0]
            self.item["curl"] = curl[0]
        else:
            self.item["cname"] = cname[1]
            self.item["curl"] = curl[1]
        

        request = Request(self.item["curl"], callback=self.parseChapterPic)
        yield request
        #return item

    def parseChapterPic(self, response):
        '''get all chapter picture'''
        page = response.body
        img = re.findall(r'src\"\:\"(.*?)\"', page)
        imgs = [base64.b64decode(i) for i in img]
        self.item["imgUrl"] = imgs
        yield self.item


class wmhSpider(Spider):

    name = "wmh"
    download_delay = 0.5

    pipeline = set([
        pipelines.wmhPipeline,
    ])

    def __init__(self):
        self.item = ManagaItem()

    start_urls = [
        'http://manhua.weibo.com/c/60592'
    ]

    def parse(self, response):
        '''get new chapter url and title'''
        sel = Selector(response)
        sites = sel.xpath('/html/body/div[3]/div[2]/div[3]/div/div')

        self.item['cname'] = sites.xpath('a/@data-chaptername').extract()[-1]
        self.item['curl'] = sites.xpath('a/@href').extract()[-1]

        request = Request(self.item['curl'], callback=self.parseChapterPic)
        yield request

    def parseChapterPic(self, response):
        '''get chapter info from Script'''
        sel = Selector(response)
        imgUrl = sel.xpath('/html/head/script[2]').extract()
        
        imgUrl = str(imgUrl[0].encode('utf8'))
        imgs = re.findall(r'\"imgUrl\"\:\"(.*?)\"\,\"\D', imgUrl)
        img = [] 
        for i in range(len(imgs)):
            imgs[i] = imgs[i].replace('.jpg', '_big.jpg').replace('\\', '')
            img.append(imgs[i])
        
        self.item['imgUrl'] = img
        
        yield self.item 
