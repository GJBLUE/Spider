# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from db.torndb import Connection
from datetime import datetime


class u17Pipeline(object):
    
    def process_item(self, item, u17Spider):
        single_managa = dict()
        db = Connection()
        
        vip_mark = item['cvip']
        if len(vip_mark) > 1:
            pass
        elif len(vip_mark) == 1:
            single_managa.setdefault('cname', item['cname'][0])
            single_managa.setdefault('curl', item['curl'][0])
        else:
            single_managa.setdefault('cname', item['cname'][-1])
            single_managa.setdefault('curl', item['curl'][-1])
        #all_managa.append(single_managa 
        sql = "insert ignore into test(cname, curl) values ('%s','%s')"%(
            single_managa['cname'].encode('utf-8', 'ignore'), single_managa['curl'].encode('utf-8', 'ignore'))
        print sql
        db.execute(sql)
        return single_managa
