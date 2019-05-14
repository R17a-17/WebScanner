# --Created by WD
# python 3.6
# coding:utf-8
'''
将爬取到的链接存储到数据库
'''



from twisted.enterprise import adbapi
import pymysql
from WebScanner.items_xss import XssItem

class MySQLAsyncPipeline:
    '''处理linkitem的链接，将所有爬取到的链接插入数据库'''
    def open_spider(self, spider):
        ''' adbapi.ConnectionPool方法可以创建一个数据库连接池对象，其中包含多个连接对象，
        每个连接对象在独立的线程中工作。adbapi只是提供了异步访问数据库的编程框架，在其
        内部依然使用MySQLdb的库访问数据库。ConnectionPool方法的第一个参数就是用来指定使用哪个库
        访问数据库，其他参数在创建连接对象时使用。'''

        db = spider.settings.get('MYSQL_DB_NAME')
        host = spider.settings.get('MYSQL_HOST')
        port = spider.settings.get('MYSQL_PORT')
        user = spider.settings.get('MYSQL_USER')
        passwd = spider.settings.get('MYSQL_PASSWORD')
        self.dbpool = adbapi.ConnectionPool('pymysql', host=host, db=db, user=user, passwd=passwd, charset='utf8')
        self.id = 1

    def close_spider(self, spider):
        self.dbpool.close()

    def process_item(self, item, spider):
        '''dbpool.runInteraction(insert_db, item)以异步方式调用instert_db函数，
        dbpool会选择连接池中的一个连接对象在独立线程中调用insert_db，其中参数
        item会被传给insert_db的第二个参数，传给insert_db的第一个参数是一个Transaction对象，
        其接口与Cursor对象类似，可以调用execute方法执行SQL语句，insert_db执行完后，连接对象
        会自动调用commit方法。'''
        self.dbpool.runInteraction(self.insert_db, item)
        return item

    def insert_db(self, tx, item):
        '''将item插入数据库的具体操作'''
        values = (
            item['vulnurl'],
            'SQLI',
        )
        sql = 'INSERT INTO t_vulninfo(vulnurl, vulntype) VALUES (%s)'
        # sql = 'INSERT INTO t_link_tmp(link) SELECT %s FROM DUAL WHERE NOT EXISTS(SELECT link from t_link_tmp where link = %s)'
        try:
            print('NNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN')
            tx.execute(sql,values)
            print('YYYYYYYYYYYYYYYYYYYYYYYYYYYY')
        except:
            pass