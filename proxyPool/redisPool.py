#!/usr/bin/env python
# coding=utf-8

import redis
from settings import redis_settings

class RedisPool(object):

    def conn(self):
        return redis.StrictRedis(password=redis_settings)

    

