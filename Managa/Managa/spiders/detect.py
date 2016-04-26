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

#        for site in sites:
#            item = ManagaItem()
#            item['cname'] = site.xpath('a/@title').extract()[-2:]
#            item['curl'] = site.xpath('a/@href').extract()[-2:]
#            item['cvip'] = site.xpath('a/@class').extract()[-2:]
#            items.append(item)
#        return items
        
        item = ManagaItem()
        item['cname'] = sites.xpath('a/@title').extract()[-2:]
        item['curl'] = sites.xpath('a/@href').extract()[-2:]
        item['cvip'] = sites.xpath('a/@class').extract()[-2:]
        return item

