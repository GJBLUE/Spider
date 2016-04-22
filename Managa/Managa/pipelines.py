# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html





class u17Pipeline(object):
    
    def process_item(self, item, u17Spider):
        all_managa = []
        single_managa = dict()
        
        print item
#        for data in item:
#            print data['cvip']
#            vip_mark = data['cvip']
#            if len(vip_mark) > 1:
#                pass
#            elif len(vip_mark) == 1:
#                single_managa.setdefault('cname', data['cname'][0])
#                single_managa.setdefault('curl', data['curl'][0])
#            else:
#                single_managa.setdefault('cname', data['cname'][-1])
#                single_managa.setdefault('curl', data['curl'][-1])
#            all_managa.append(single_managa)

        vip_mark = item['cvip']
        if len(vip_mark) > 1:
            pass
        elif len(vip_mark) == 1:
            single_managa.setdefault('cname', item['cname'][0])
            single_managa.setdefault('curl', item['curl'][0])
        else:
            single_managa.setdefault('cname', item['cname'][-1])
            single_managa.setdefault('curl', item['curl'][-1])
        #all_managa.append(single_managa)
        return single_managa
