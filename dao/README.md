## DAO  数据库


### 负责MySQL、 MongoDB和Redis的初始化与连接，数据库相关写法上是通用的。

####  mongo_db.py
#### mysql_entity.py
定义MySQL的实体类，即定义MySQL中数据表格的列头，列头应该与利用爬虫抓取到MySQL中的列头一致。
#### mysql_db.py
Base = declarative_base()

self.engine = create_engine()

self._DBSession = sessionmaker(bind = self.engine)
#### redis_db.py

redis.StrictRedis() 方法 传进Redis数据库的账号密码port等登陆信息即可