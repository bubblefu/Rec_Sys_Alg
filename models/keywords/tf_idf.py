#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
    @Time :    2020/12/23 15:56
    @Author:   Paopao Fu
    @File:     tf_idf.py
    @Software: PyCharm
    @Purpose:  利用文档找反文档词频，提取关键词，词频，
                调用jieba分词库进行分词，有三种模式，普通模式，全切分模式还有 搜索引擎模式
                在RS里用全切分模式
"""
'''
 TF-IDF:
 1. 分词  一般用jieba
 2. 针对整个语料库，去统计逆文档频率
 3. 排序 
 4. 关键词提取（倒序的top-N）
'''
# jieba的处理：1.停用词 介词连接词 都没用 得去掉  2. 只要名词 动名词这种有意义的词
# trick1 能用双引号就用双引号，用单引号的话，在一些用go等语言的情况，就不会被认作json格式

import jieba.posseg as pseg
import jieba
import jieba.analyse
import os
import re


class Segment(object):
    def __init__(self, stopword_files=[], userdict_files=[], jieba_temp_dir=None):  # 定义停用词文件，定义用户字典文件
        if jieba_temp_dir:
            jieba.dt.tmp_dir = jieba_temp_dir
            if not os.path.exists(jieba_temp_dir):  # 如果系统不存在这个临时文件，就创建一下
                os.makedirs(jieba_temp_dir)
        self.stopwords = set()
        for stopword_file in stopword_files:
            with open(stopword_file, "r", encoding="utf-8") as rf:
                for row in rf.readlines():
                    word = row.strip()
                    if len(word) > 0:
                        self.stopwords.add(word)   # 添加到停用词列表里
        for userdict in userdict_files:
            jieba.load_userdict(userdict)


    def cut(self, text):
        word_list = []
        text.replace('\n', '').replace('\u3000', '').replace('\u00A0', '') # 切词 首先替换一些空格，这种写法得记住
        text = re.sub('[a-zA-Z0-9.。,，：:!]', '', text) # 用re.sub库把句子里的一些数字和标点去掉，因为这是给中文做分词
        words = pseg.cut(text)   # 分词，就是在jieba.posseg库中
        print(words)
        # 把words 添加到word_list中
        for word in words:
            # print(word.word, word.flag)
            # wor = i.strip()
            if word in self.stopwords or len(word) == 0:
                continue
            word_list.append(word)
        return word_list

    def extract_keyword(self, text, alg='tf-idf', use_pos=True): # use_pos 要不要过滤词性
        text = re.sub('[a-zA-Z0-9.。,，：:!]', '', text)
        if use_pos:
            allow_pos = ('n', 'nr', 'ns', 'vn', 'v') # 允许名词动名词什么的
        else:
            allow_pos = ()
        if alg =='tf-idf':
            tags = jieba.analyse.extract_tags(text, withWeight=False)
        elif alg == 'textrank':
            tags = jieba.analyse.textrank(text, withWeight=True, allowPOS=allow_pos)
        return tags


if __name__ == '__main__':
    seg = Segment(stopword_files=[], userdict_files=[])
    text = "所以暂时将你眼睛闭了起来" \
           "黑暗之中漂浮我的期待" \
           "平静脸孔映着缤纷色彩" \
           "让人好不疼爱你" \
           "可以随着我的步伐轻轻柔柔的踩" \
           "将美丽的回忆慢慢重来" \
           "突然之间浪漫无法释怀" \
           "明天我要离开" \
           "你给的爱" \
           "无助的等待" \
           "是否我一个人走" \
           "想听见你的挽留" \
           "春风秋雨飘飘落落只为寂寞" \
           "你给的爱" \
           "甜美的伤害" \
           "深深的锁住了我" \
           "隐藏不住的脆弱" \
           "泛滥河水将我冲向你的心头"
    # print(seg.extract_keyword(text, use_pos=True))
    # print(seg.cut(text))
    textrank = seg.extract_keyword(text, alg='textrank', use_pos=True)[:6]
    tfidf =  seg.extract_keyword(text, alg='tf-idf', use_pos=True)[:6]
    # ！！！set的做法，在企业中叫做算法联合，企业中常用，就是取这两种算法的交集，即这两种算法都认为是关键词的一部分，！！！
    print(set(textrank + tfidf))  # 取set交集，在python 中常见