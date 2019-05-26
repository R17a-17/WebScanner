#--Created by WD
#python 3.6
#coding:utf-8

#########################尝试生成一个可拓展性漏洞探测脚本########################

from scrapy import *
from pymysql import *

class VulnDetectSpider(Spider):
    '''漏洞探测：对每个URL进行测试，包括xss、sqli、Weakpassword、CSRF'''
    #爬虫命名
    name = 'VulnDetectSpider'

    def __init__(self):
        self.linkth = 1
        # 将得到的Connection对象和Cursor对象分别赋值给self.db_conn和self.db_cur，以便之后使用。
        db_conn = connect(host='localhost', port=3306, db='webscanner', user='root', passwd='toor', charset='utf8')
        self.db_cur = db_conn.cursor()
        self.detect_code = None

    def parse(self):
        pass