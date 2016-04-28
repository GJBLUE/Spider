#!/usr/bin/env python
# coding=utf-8

from scrapy.spider import Spider
from scrapy.selector import Selector
from Managa.items import ManagaItem


class u17Spider(Spider):

    name = "u17"
    allowed_domains = ["u17.com"]

    start_urls = [
        "http://www.u17.com/comic/190.html",
        "http://www.u17.com/comic/195.html"
    ]

    def parse(self, response):
        sel = Selector(response)
        sites = sel.xpath('//*[@id="chapter"]/li')

        
        item = ManagaItem()
        cname = sites.xpath('a/@title').extract()[-2:]
        curl = sites.xpath('a/@href').extract()[-2:]
        cvip = sites.xpath('a/@class').extract()[-2:]
        
        if cvip[-1] == 'vip_chapter':
            item["cname"] = cname[0]
            item["curl"] = curl[0]
        else:
            item["cname"] = cname[1]
            item["curl"] = curl[1]
        
        #print item
        return item

