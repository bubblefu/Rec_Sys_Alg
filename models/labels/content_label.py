#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
    @Time :    2020/12/23 15:10
    @Author:   Paopao Fu
    @File:     content_label.py
    @Software: PyCharm
    @Purpose:  内容画像系统
"""


import re
from datetime import datetime
from sqlalchemy import distinct
from dao.mongo_db import MongoDB
from dao.mysql_db import MySql
from dao.mysql_entity import Content
from models.keywords.tf_idf import Segment



class ContentLabel(object):
    def __init__(self):
        self.seg = Segment(stopword_files=[], userdict_files=[])
        # 连接到MySQL,标准写法
        self.engine = MySql()
        self.session = self.engine._DBSession()
        # 连接到MongoDB
        self.mongo = MongoDB(db='sina_news_rec_db')  # 选择MongoDB连接到的database叫sina_news_rec_db
        self.sina_news_rec_db = self.mongo.sina_news_rec_db
        # 声明MongoDB选定数据库中要使用的collection的名字
        self.collection = self.sina_news_rec_db['content_labels']

    def get_data_from_mysql(self):
        '''
        distinct是查询功能，根据实体类里定义的type字段查询data中不同的地方(也可以根据时间等其他字段！)
        这个distinct 对于千万数量级的数据也能比较快
        因为type只有几类，那查询每一类data的内容可以更加灵活简单一些
        综述 ： 通过distinct方法，先拿到type，通过选择新闻的type，根据type查询里边的数据，每一个数据再存到content_collection里
        :return:
        '''
        # 1. 根据type拿数据
        types = self.session.query(distinct(Content.type))
        # 2. 查询,通过.filter方法
        for type in types:
            res = self.session.query(Content).filter(Content.type ==type[0])
            if res.count() > 0:  # 若里面有数据：
                # 3. 取数据
                for x in res.all():
                    keywords = self.get_keywords(x.content, 10)
                    word_nums = self.get_words_nums(x.content)
                    times = x.times
                    create_time = datetime.utcnow()
                    # content_collection要存到MongoDB里 下面操作一定要放到for 里边，否则会报错：id值重复
                    content_collection = dict()   # 内容画像列表，这是要插入到MongoDB中的
                    content_collection['describe'] = x.content
                    content_collection['keywords'] = keywords
                    content_collection['word_num'] = word_nums
                    content_collection['news_date'] = times
                    # 根据用户的行为，有不同的热度，热度会变化的。这里10000都是给的初始的热度
                    content_collection['hot_heat']  = 10000
                    content_collection['type'] = x.type
                    content_collection['create_time'] = create_time
                    # 把内容画像存入到content_collection字典里后，插入到MongoDB中
                    self.collection.insert_one(content_collection)

    def get_keywords(self, contents, nums=10):
        keywords = self.seg.extract_keyword(contents)[:nums]
        return keywords

    def get_type(self):
        return

    def get_news_time(self):
        return

    def get_words_nums(self, contents):
        ch = re.findall('[\u4e00-\u9fa5]', contents)
        nums = len(ch)
        return nums



if __name__ == '__main__':
    test = ContentLabel()
    # article = '柴屁屁是我的大宝宝，呱呱，我真是爱她'
    # print(test.get_words_nums(article))
    print(test.get_data_from_mysql())