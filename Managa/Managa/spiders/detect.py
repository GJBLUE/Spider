#!/usr/bin/env python
# coding=utf-8

from scrapy.spider import Spider, Request
from scrapy.selector import Selector
from Managa.items import ManagaItem

import base64
import re


class u17Spider(Spider):

    name = "u17"
    allowed_domains = ["u17.com"]

    start_urls = [
        "http://www.u17.com/comic/190.html",
        "http://www.u17.com/comic/195.html"
    ]
    
    def __init__(self):
        self.item = ManagaItem()

    def parse(self, response):
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
        page = response.body
        img = re.findall(r'src\"\:\"(.*?)\"', page)
        imgs = [base64.b64decode(i) for i in img]
        self.item["imgUrl"] = imgs
        yield self.item

