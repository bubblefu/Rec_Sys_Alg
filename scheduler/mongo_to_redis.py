#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
    @Time :    2020/12/24 13:42
    @Author:   Paopao Fu
    @File:     mongo_to_redis.py
    @Software: PyCharm
    @Purpose:  定时任务：把储存在mongo的内容画像数据，传到Redis里，因为在生产环境中，Redis会快
"""


from dao.redis_db import Redis
from dao.mongo_db import MongoDB


class Write_to_Redis():
    def __init__(self):
        # 初始化Redis
        self._redis = Redis()
        # 初始化MongoDB，声明类并选择数据库 ，并选择数据库中的collection
        self.mongo = MongoDB(db='sina_news_rec_db')
        self.sina_news_rec_db = self.mongo.sina_news_rec_db
        self.collection = self.sina_news_rec_db['content_labels']
    # 从MongoDB里取数据，按照一定的顺序排序，再存到Redis里边
    def get_from_mongodb(self):
        # pipline的写法要注意，在py里是需要加$的
        # 设置一个group的主键，类型是type，以_id来表示
        piplines = [
            {
                '$group' : {
                    '_id' : "$type"
                }
            }
        ]
        # 在mongodb里取type，用到的是.aggregate(piplines)
        types = self.collection.aggregate(piplines)
        count = 0
        # 对 type进行查询，在MongoDB里用find方法，首先创造查询条件--> find(search_type)
        for type in types:
            search_type = {"type": type['_id']}
            data = self.collection.find(search_type)
            # 查询到data后，放到Redis里。
            # 放到Redis里的内容，就是可能放入到Android APP里的内容
            for info in data:
                # 把内容先放到Redis_results里，再把这个dict存到Redis
                redis_results = dict()
                redis_results['describe'] = info['describe']
                redis_results['type'] = info['type']
                redis_results['news_date'] = info['news_date']
                # redis_results['describe'] = info['describe']
                # redis_results['describe'] = info['describe']
                # redis_results['describe'] = info['describe']
                # redis_results['describe'] = info['describe']
                # 用redis 的set()方法来存到redis!!!!!
                self._redis.redis.set("news_detail:" + str(info['_id']), str(redis_results))
                # 删除这个redis 的db里的数据，和上一句话可以分别来使用
                # self._redis.redis.delete(str(info['_id']))
                if count% 100 == 0:  # 为了看进度
                    print(count)
                count += 1


if __name__ == '__main__':
    write_to_redis = Write_to_Redis()
    write_to_redis.get_from_mongodb()
