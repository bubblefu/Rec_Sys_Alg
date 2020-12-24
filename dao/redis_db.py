#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
    @Time :    2020/12/23 19:33
    @Author:   Paopao Fu
    @File:     redis_db.py
    @Software: PyCharm
    @Purpose:  
"""
import redis


class Redis:
    def __init__(self):
        self.redis = redis.StrictRedis(host='r-m5e8kd481g3boqztfhpd.redis.rds'
                                            '.aliyuncs.com',
                                       port=6379,
                                       password='Ipeaking123',
                                       decode_responses=True,
                                       db=18)
