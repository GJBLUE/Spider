# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

#from db.torndb import Connection
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


class wmhPipeline:
    
    @check_spider_pipeline
    def process_item(self, item, wmhSpider):
        return item
