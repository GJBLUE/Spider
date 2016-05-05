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
    

    def parse(self, response):
        '''get new chapter'''

        
        item = ManagaItem() 

        sel = Selector(response)
        site = sel.xpath('//*[@id="chapter"]/li')
        cname = site.xpath('a/@title').extract()[-2:]
        curl = site.xpath('a/@href').extract()[-2:]
        cvip = site.xpath('a/@class').extract()[-2:]
        
        
        if cvip != []:
            item["cname"] = cname[0]
            item["curl"] = curl[0]
        else:
            item["cname"] = cname[-1]
            item["curl"] = curl[-1]
        
        #yield self.item
        
        request = Request(item["curl"], 
                        callback=self.parseChapterPic,
                        meta={"item":item} ) 
        yield request

    def parseChapterPic(self, response):
        '''get all chapter picture'''
       
        item = response.meta["item"]       

        page = response.body
        img = re.findall(r'src\"\:\"(.*?)\"', page)
        imgs = [base64.b64decode(i) for i in img]
        item["imgUrl"] = imgs
        
        yield item


class wmhSpider(Spider):

    name = "wmh"
    download_delay = 0.5

    pipeline = set([
        pipelines.wmhPipeline,
    ])


    start_urls = [
        'http://manhua.weibo.com/c/60592'
    ]

    def parse(self, response):
        '''get new chapter url and title'''


        item = ManagaItem()

        sel = Selector(response)
        sites = sel.xpath('/html/body/div[3]/div[2]/div[3]/div/div')

        item['cname'] = sites.xpath('a/@data-chaptername').extract()[-1]
        item['curl'] = sites.xpath('a/@href').extract()[-1]

        request = Request(item['curl'], 
                          callback=self.parseChapterPic,
                          meta={"item":item}
                          )
        yield request

    def parseChapterPic(self, response):
        '''get chapter info from Script'''  

        item = response.meta["item"] 
        sel = Selector(response)
        imgUrl = sel.xpath('/html/head/script[2]').extract()
        
        imgUrl = str(imgUrl[0].encode('utf8'))
        imgs = re.findall(r'\"imgUrl\"\:\"(.*?)\"\,\"\D', imgUrl)
        img = [] 
        for i in range(len(imgs)):
            imgs[i] = imgs[i].replace('.jpg', '_big.jpg').replace('\\', '')
            img.append(imgs[i])
        
        item['imgUrl'] = img
        
        yield item 
