#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
    @Time :    2020/12/24 14:33
    @Author:   Paopao Fu
    @File:     simple_rec_by_newest_time.py
    @Software: PyCharm
    @Purpose:  最简单的推荐，即通过时间，时间越新越在推荐列表前面。这个列表是最终要在app展示
                这只是一个demo，为了跑通推荐系统，后期会把推荐算法逐渐加入。
"""

from dao.redis_db import Redis
from dao.mongo_db import MongoDB


class SimpleRec_by_Newest_Time:
    def __init__(self):
        self._redis = Redis()
        self.mongo = MongoDB(db='sina_news_rec_db')
        self.sina_news_rec_db = self.mongo.sina_news_rec_db
        self.collection = self.sina_news_rec_db['content_labels']

    def get_news_order_by_time(self):
        # 把所有的东西都查出来，并根据news_date 排序，倒序排 注意！！！sort的写法与ROBO3T不同
        # ROBO3T中的操作是：db.getCollection('content_labels').find().sort({
        # "news_date": -1})
        # 注意哈：data是在MongoDB里倒序的取
        data = self.collection.find().sort([{"$news_date", -1}])
        count = 3000
        # 进行插入到Redis的操作
        for news in data:
            # zadd 传进去一个键值对，设为内容和分数 : {str(news['_id']):count
            # 其中，"rec_by_time_list" 是新建了一个redis的DB 名字,一个一个的往redis里插入，
            # 结果在redis里形成一个表，是 id: score的形式，这个count就是score的意思
            # 因为这只是简单的时间逆序排序，排序的表的评分就越新的新闻score越多
            self._redis.redis.zadd("rec_by_time_list",
                                   {str(news['_id']): count})
            count -= 1
            if count % 10 == 0:
                print(count)


if __name__ == '__main__':
    simple = SimpleRec_by_Newest_Time()
    simple.get_news_order_by_time()
