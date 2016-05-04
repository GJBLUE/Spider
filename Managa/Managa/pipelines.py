# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from db.torndb import Connection
from decorator import check_spider_pipeline

class u17Pipeline(object):
    
    @check_spider_pipeline    
    def process_item(self, item, u17Spider):
        db = Connection()
        
        sql = "insert ignore into test(cname, curl) values ('%s','%s')"%(
            item['cname'].encode('utf-8', 'ignore'), item['curl'].encode('utf-8', 'ignore'))
        print sql
        db.execute(sql)
        return item

class wmhPipeline:
    
    @check_spider_pipeline
    def process_item(self, item, wmhSpider):
        return item
