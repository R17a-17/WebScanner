# --Created by WD
# python 3.6
# coding:utf-8

from scrapy import *
from pymysql import *
import re
from scrapy.conf import settings
import random
from WebScanner.items_crlf import CrlfItem


class CRLF_Spider(Spider):
    '''针对每个页面做出http响应头拆分探测特征码请求，然后根据响应包进行响应包特征码的探测'''

    name = 'CRLFSpider'
    custom_settings = {
        'ITEM_PIPELINES': {'WebScanner.pipelines_mysqldb_crlfvulninfo.CrlfPipeline': 300,}
    }

    def __init__(self):
        self.linkth = 1
        # 将得到的Connection对象和Cursor对象分别赋值给self.db_conn和self.db_cur，以便之后使用。
        db_conn = connect(host='localhost', port=3306, db='webscanner', user='root', passwd='toor', charset='utf8')
        self.db_cur = db_conn.cursor()
        self.detect_code = None

    def start_requests(self):
        '''重写starturl的请求'''
        # 开始url
        self.start_urls = []
        self.url = self.geturlfrommysql(self.linkth)
        self.url = self.crlf_detect()
        self.start_urls.append(self.url)
        # 设置cookie便于访问登录后的页面
        self.cookie = settings['COOKIES']
        yield Request(self.start_urls[0], callback=self.parse, cookies=self.cookie)

    def parse(self, response):
        ''''''

        if self.detect_code == None:
            print('>>>no injection point')
        else:
            if self.crlf_check(response.headers):
                print('>>>crlf')
                crlfitem = CrlfItem()
                crlfitem['vulnurl'] = self.url
                crlfitem['vulntype'] = 'CRLF'
                yield crlfitem
            else:
                print('>>>no crlf')

        self.linkth = self.linkth + 1
        self.url = self.geturlfrommysql(self.linkth)

        if self.url:
            # 如果找到下一页的URL，构造新的Request 对象
            yield Request(self.url, callback=self.parse, cookies = self.cookie,dont_filter=True)





    def crlf_detect(self):
        '''生成crlf探测码'''
        url = self.url
        #匹配参数和值,放入字典list
        list = []
        for match in re.finditer(r"((\A|[?&])(?P<parameter>[\w]+)=)(?P<value>[^&]+)", url):
            list.append({'parameter':match.group('parameter'),'value':match.group('value')})
        #在最后一个参数后面添加探测码
        if len(list) > 0:
            i = len(list) - 1
            parameter = list[i]['parameter']
            value = list[i]['value']
            self.detect_code = '%0D%0A%20webscanCustomInjectedHeader%3A$20injectedbywd'
            oldstr = parameter + '=' + value
            value1 = value + self.detect_code
            # 参数和探测值生成新的字符串
            newstr = parameter + '=' + value1
            url = url.replace(oldstr, newstr)
        else:
            self.detect_code = None
        return url

    def crlf_check(self, headers):
        '''检测是否存在响应特征码'''

        if 'webscanCustomInjectedHeader' in headers and 'injectedbywd' in headers:
            return True
        else:
            return False




    def geturlfrommysql(self, linkth):
        '''从数据库获取要检测的url'''
        sql = 'select link from t_link_tmp where id=%s'
        self.db_cur.execute(sql, linkth)
        try:
            nextlink = self.db_cur.fetchone()[0]
        except:
            nextlink = None
        return nextlink
