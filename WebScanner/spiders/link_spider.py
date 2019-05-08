#--Created by WD
#python 3.6
#coding:utf-8

from scrapy import *
from scrapy.linkextractors import LinkExtractor
from urllib.parse import urlparse
from ..items_link import LinkItem
from pymysql import *
# import scrapy
# from scrapy.crawler import CrawlerProcess
# import sys,os
# sys.path.append(os.path.dirname(__file__) + os.sep + '../')

class LinkSpider(Spider):
    '''根据指定的目标爬取网站的所有链接'''

    #给爬虫命名
    name = 'LinkSpider'
    #指定爬取的开始链接
    # start_urls = ["http://books.toscrape.com/"]
    #获取目标的域名
    allow_domain = []
    # allow_domain.append(urlparse(start_urls[0]).netloc)
    #爬取最大限制数
    max_crawl = 3000
    #爬取的行数，即爬取到第几个链接
    linkth = 1

    # 将得到的Connection对象和Cursor对象分别赋值给self.db_conn和self.db_cur，以便之后使用。
    db_conn = connect(host='localhost', port=3306, db='webscanner', user='root', passwd='toor', charset='utf8')
    db_cur = db_conn.cursor()

    def __init__(self, *args, **kwargs):
        super(LinkSpider, self).__init__(*args, **kwargs)
        #命令行指定start_url
        self.start_urls =  [kwargs.get('start_url')];
        self.allow_domain.append(urlparse(self.start_urls[0]).netloc)


    def parse(self, response):
        #连接数据库
        # db = conn.connsql()
        #使用cursor()方法获取操作游标
        # cursor = db.cursor()

        #提取开始链接的页面中 所有属于目标域的URL
        links = LinkExtractor(allow_domains = self.allow_domain).extract_links(response)

        #将提取的链接插入数据库
        for link in links:
            linkitem = LinkItem()
            linkitem['link'] = link.url
            yield linkitem

        next_url = self.select_db(self.linkth)
        print(next_url)

        if next_url and self.linkth < self.max_crawl:
            self.linkth = self.linkth + 1
            print(self.linkth )
            #如果找到下一页的URL，构造新的Request 对象
            yield Request(next_url, callback=self.parse)
        else:
            self.db_conn.close()

    def select_db(self, linkth):
        '''查询链接'''
        sql = 'select link from t_link_tmp where id=%s'
        self.db_cur.execute(sql, linkth)
        try:
            nextlink = self.db_cur.fetchone()[0]
        except:
            nextlink = None
        return nextlink


# process = CrawlerProcess({
#     'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
# })
# process.crawl(LinkSpider)
# process.start() # the script will block here until the crawling is finished