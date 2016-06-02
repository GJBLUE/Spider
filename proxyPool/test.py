#!/usr/bin/env python
# coding=utf-8

from redisPool import RedisPool
from settings import redis_settings

def test():
    db = RedisPool().conn()
    db.delete('moba')
    print db.get('moba')

if __name__ == "__main__":
    test()
