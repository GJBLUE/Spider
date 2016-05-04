#!/usr/bin/env python
# coding=utf-8

import functools

def check_spider_pipeline(process_item_method):
    ''''''

    @functools.wraps(process_item_method)
    def wrapper(self, item, spider):
        
        if self.__class__ in spider.pipeline:
            return process_item_method(self, item, spider)
        else:
            return item

    return wrapper

