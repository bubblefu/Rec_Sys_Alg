#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
    @Time :    2020/12/23 13:47
    @Author:   Paopao Fu
    @File:     mongo_db.py
    @Software: PyCharm
    @Purpose:  连接MongoDB数据库
"""

import pymongo


class MongoDB(object):
    def __init__(self, db):  # 在内部已经定义好了MongoDB账号(本地or云)外部调用直接传入数据库名称即可
        # 定义初始化方法
        # 写在init里，节省内存开销
        # mongo_client = self._connect('47.104.154.74', '21999', '', '', db)
        mongo_client = self._connect('localhost', '27017', '', '',
                                     db)  # 遍历数据库连接
        self.sina_news_rec_db = mongo_client[db]  # 选择MongoDB数据库

    # 定义连接方法
    def _connect(self, host, port, user, pwd, db):
        mongo_info = self._splicing(host, port, user, pwd,
                                    db)  # 正常讲是MongoDB连接用到的字符串
        mongo_client = pymongo.MongoClient(mongo_info, connectTimeoutMS=12000,
                                           connect=False)
        # connect = False 如果为true的话，每次都会重连，就会耗时，会有几次连接不上，所以设置为false
        # connectTimeoutMS 连接超时时间
        return mongo_client

    # mongoDB 可以不传密码
    @staticmethod
    def _splicing(host, port, user, pwd, db):
        client = 'mongodb://' + host + ':' + str(port) + '/'  # 是个正常连接方式
        if user != '':  # 用户名不为空，那就再加上用户名
            client = 'mongodb://' + user + ':' + pwd + '@' + host + ':' + str(
                port) + '/'
            if db != '':  # 如果db 不是空的，就得在client后加入db。
                client += db
        return client

    # def test_insert(self):
    #     testcollection = dict()
    #     testcollection['name'] = 'fupaopao'
    #     testcollection['lover'] = 'chaipipi'
    #     self.collection_test.insert_one(testcollection)

# if __name__ == '__main__':
#     test = MongoDB(db='test')
#     test.test_insert()
