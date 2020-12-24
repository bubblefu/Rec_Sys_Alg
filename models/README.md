模型文件，进行召回和排序

keywords:关键词提取相关
labels : 标签系统
recall : 排序
rank
rerank



/labels/content_label.py：

      构建item、即新闻的简单内容画像（新闻id , 正文，关键词，词总数，新闻日期，热度值，新闻类型，创建时间等）
      数据走向：  MySQL ---> content_label.py ---> MongoDB ----->mongo_to_redis.py-----> Redis
                  取            构建内容画像          放                       把文章详情写到article_details来，把推荐列表写到rec
      数据处理：
        1. 初始化MySQL 和MongoDB数据库
        2. get_data_from_mysql()
            2.1    