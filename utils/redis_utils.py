#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/5/26 10:52
# @Name    : peilun
# @File    : redis_utils.py
# @Software: PyCharm
from comment.acquire_config import con
import redis

def get_conn():
    redis_host = con.redis_host
    redis_port = con.redis_port
    redis_db = con.redis_db
    redis_pwd = con.redis_pwd

    return redis.Redis(host=redis_host, port=redis_port, password=redis_pwd, db=redis_db, decode_responses=True)


# redis不执行回收策略，不会失效的那种
def set(key, value):
    conn = get_conn()
    conn.set(key, value)


# set且加上失效时间
def set_with_expireTime(key, value, second):
    conn = get_conn()
    conn.set(key, value, ex=second)


# 根据key获取健值
def get(k):
    conn = get_conn()
    return conn.get(k)


# 根据key删除健值
def remove(k):
    conn = get_conn()
    return conn.delete(k)
