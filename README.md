# 一个新闻推荐系统~~~
Code for an enterprise recommendation system

建立内容画像系统





1. DAO 

    与数据库操作相关联的东西  
		    Data Access Object
2. Modules
   
    模型文件，召回、排序、关键词提取，textrank ，tfidf都是在这里做
        labels存取用户画像
    
3. constant

    定义常量，可以放入config里，也可以不用这个
4. scheduler 

    调度 做定时任务的东西，少则3-5个，多则几十个。任何推荐系统都需要
5. util  

    工具类，做项目时需要各种各样的需要处理的操作，都会通过它去做

6. Config  
        配置文件，做项目过程中，经常做一些配置变更