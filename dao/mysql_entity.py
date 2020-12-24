#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
    @Time :    2020/12/24 12:23
    @Author:   Paopao Fu
    @File:     mysql_entity.py
    @Software: PyCharm
    @Purpose:  要在content_label.py里导入和MySQL相关的内容，所以需要对MySQL进行查询，查询的话就
               需要一个实体类，这里就定义 MySQL 的table实体类
"""
from sqlalchemy import Column, Integer, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base

from dao.mysql_db import MySql

Base = declarative_base()


class Content(Base):
    __tablename__ = 'data'
    # trick： id times title等数据库的列名的定义，必须和数据库中一致，差一点都不行
    id = Column(Integer(), primary_key=True)
    times = Column(DateTime())
    title = Column(Text())
    content = Column(Text())
    type = Column(Text())

    def __init__(self):
        mysql = MySql()
        engine = mysql.engine
        Base.metadata.create_all(engine)
