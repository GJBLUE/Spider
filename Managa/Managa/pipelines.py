# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

#from db.torndb import Connection

import scrapy

from scrapy.contrib.pipeline.images import ImagesPipeline
from scrapy.exceptions import DropItem
from decorator import check_spider_pipeline
from twisted.enterprise import adbapi
from settings import db

class u17Pipeline(object):
   

    def __init__(self, dbpool):
        self.dbpool = dbpool

    
    @classmethod
    def from_settings(cls, settings):
        """loading mysql settings"""
        
        dbargs = dict( 
            host=db["host"],
            port=db["port"],
            db=db["dbname"],
            user=db["user"],
            passwd=db["passwd"],
            charset="utf8"
            )

        dbpool = adbapi.ConnectionPool("MySQLdb", **dbargs)
        return cls(dbpool)

    
    @check_spider_pipeline    
    def process_item(self, item, u17Spider):
        
        
        # run database query in the thread pool
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error)

        return query


    def do_insert(self, conn, item):
        

        sql = "insert ignore into test(cname, curl) values ('%s','%s')"%(
            item['cname'].encode('utf-8', 'ignore'), item['curl'].encode('utf-8', 'ignore'))
        print sql
        conn.execute(sql)
        
        return item
        #return item


    def handle_error(self, e):
        print e 


class imagesPipeline(ImagesPipeline):
    
    def get_media_requests(self, item, info):
        for image_url in item["imgUrl"]:
            yield scrapy.Request(image_url, meta={'item':item})


    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        return item

    def file_path(self, request, response=None, info=None):
        item = request.meta['item']
        image_guid = request.url.split('/')[-1]
        filename = u'{0}/{1}'.format(item['cname'], image_guid)
        return filename


class wmhPipeline:


    @check_spider_pipeline
    def process_item(self, item, wmhSpider):
        return item
