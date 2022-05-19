# -*- encoding: utf-8 -*-
from flask import g
# 导入redis
from database import RedisClient


def get_redis() -> 'RedisClient':
    '''这里使用到全局变量g'''
    if g.get("redis") is None:
        g.redis = RedisClient()
    return g.redis