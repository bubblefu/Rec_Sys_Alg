#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
    @Time :    2020/12/23 19:29
    @Author:   Paopao Fu
    @File:     mysql_db.py
    @Software: PyCharm
    @Purpose:  连接MySql数据库
"""
import sys
sys.path.append('..') # 防止在服务器端部署时，路径不同引起的错误
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


class MySql():
    def __init__(self):
        Base = declarative_base()
        self.engine = create_engine("mysql+pymysql://root:1413@localhost:3306/sina4", encoding='utf-8')
        self._DBSession = sessionmaker(bind = self.engine)