# --Created by WD
# python 3.6
# coding:utf-8

from scrapy import *
from scrapy.linkextractors import LinkExtractor
from urllib.parse import urlparse
from WebScanner.items_link import LinkItem
from pymysql import *
from scrapy.conf import settings
import re
from scrapy.crawler import CrawlerProcess
import chardet


class TestSpider(Spider):
    '''根据指定的目标爬取网站的所有链接'''

    # 给爬虫命名
    name = 'TestSpider'
    # 为每个spider指定对应的pipelines
    custom_settings = {
        'ITEM_PIPELINES': {'WebScanner.pipelines_mysqldb_linktable.LinkPipeline': 300}
    }
    # 指定爬取的开始链接
    # start_urls = ["http://books.toscrape.com/"]
    # 获取目标的域名
    allow_domain = []
    # allow_domain.append(urlparse(start_urls[0]).netloc)
    # 爬取最大限制数
    max_crawl = 3000
    # 爬取的行数，即爬取到第几个链接
    linkth = 1

    # 将得到的Connection对象和Cursor对象分别赋值给self.db_conn和self.db_cur，以便之后使用。
    db_conn = connect(host='localhost', port=3306, db='webscanner', user='root', passwd='toor', charset='utf8')
    db_cur = db_conn.cursor()

    def __init__(self, *args, **kwargs):
        super(TestSpider, self).__init__(*args, **kwargs)
        # 命令行指定start_url
        self.start_urls = [kwargs.get('start_url')]
        self.allow_domain.append(urlparse(self.start_urls[0]).netloc)

    def start_requests(self):
        '''重写starturl的请求'''

        # 设置cookie便于访问登录后的页面
        self.cookie = settings['COOKIES']
        yield Request(self.start_urls[0], callback=self.parse, cookies=self.cookie,dont_filter=True)

    def parse(self, response):
        # 连接数据库
        # db = conn.connsql()
        # 使用cursor()方法获取操作游标
        # cursor = db.cursor()

        # 提取开始链接的页面中 所有属于目标域的URL
        deny_parttern = '.+(delete|remove|stop|undeploy|reload|restart|' \
                        'logout|signout|logoff|signoff|exit|quit|byebye|bye-bye|clearuser|invalidate|setup|reset).+'
        links = LinkExtractor(allow_domains=self.allow_domain, deny=deny_parttern).extract_links(response)

        # 将提取的链接插入数据库
        for link in links:
            linkitem = LinkItem()
            linkitem['link'] = link.url
            yield linkitem

        self.linkth = self.linkth + 1
        next_url = self.select_db(self.linkth)

        if next_url and self.linkth < self.max_crawl:

            # 如果找到下一页的URL，构造新的Request 对象
            yield Request(next_url, callback=self.parse, cookies=self.cookie,dont_filter=True)
        else:
            #探测带参数的url
            self.linkth = 1
            next_url = self.select_db(self.linkth)
            if next_url:
                yield Request(next_url, callback=self.form_parse, cookies=self.cookie, dont_filter=True)
            else:
                self.db_conn.close()


    def form_parse(self, response):

        # 根据需求转化 response.encoding

        formdata = self.form_find(response.body.decode(response.encoding))
        print(len(formdata))
        if len(formdata) == 0:
            self.linkth = self.linkth + 1
            next_url = self.select_db(self.linkth)
            print(next_url)
            if next_url:
                yield Request(next_url, callback=self.form_parse, cookies=self.cookie, dont_filter=True)
            else:
                self.db_conn.close()
            return
        else:
            linkitem = LinkItem()
            linkitem['link'] = response.url+'?' +formdata{0}
            yield linkitem

    def test(self,response):
        print('hi')

    def after_detect(self, response):
        '''check login succeed before going on'''
        print('88888888888888888888888888')
        linkitem = LinkItem()
        linkitem['link'] = response.url
        yield linkitem
        print('9999999999999999999999999999999')
        self.linkth = self.linkth + 1
        next_url = self.select_db(self.linkth)
        print(next_url)

        if next_url:
            # 如果找到下一页的URL，构造新的Request 对象
            yield Request(next_url, callback=self.form_parse, cookies=self.cookie, dont_filter=True)


    def form_find(self, html):
        '''在登录页面的响应中找到form表单，并根据表单属性等获取fromdata'''


        parameter_list = []
        tgtform = ''
        # 匹配form表单列
        formmatch = re.finditer('<form.*>([\s\S])*</form>', html)
        if formmatch == None:
            return None
        for form in formmatch:
            tgtform = form.group()

        inputmatch = re.finditer('<input[^>]+>', tgtform)
        if inputmatch == None:
            return parameter_list
        # 匹配form里面的所有参数和值
        for q in inputmatch:
            namematch = re.finditer('name="(?P<name>[^ ]+)"', q.group())
            if namematch == None:
                break
            else:
                for match in namematch:
                    name = match.group('name')
                valuematch = re.finditer('value="(?P<value>[^ ]+)"', q.group())
                value = '1'
                if valuematch != None:
                    for match1 in valuematch:
                        value = match1.group('value')
                parameter_list.append({'name':name,'value': value})
                # formdatalist.append(parameter_list)
        print('@@@@@@@@@@@@@@@@@@@@@@@@@@@',parameter_list)
        return parameter_list

    #######################################################

    def select_db(self, linkth):
        '''查询链接'''
        sql = 'select link from t_link_tmp where id=%s'
        self.db_cur.execute(sql, linkth)
        try:
            nextlink = self.db_cur.fetchone()[0]
        except:
            nextlink = None
        return nextlink
    #############################################################


def main(url):
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })
    process.crawl(TestSpider,start_url=url)
    process.start() # the script will block here until the crawling is finished
    # scrapy.cmdline.execute(('scrapy crawl WeakpwdSpider -a start_url='+url[0]).split())  # 这就是我们在命令行中的代码

if __name__ == '__main__':
    main('http://192.168.177.161/dvwa/index.php')























# --Created by WD
# python 3.6
# coding:utf-8

from scrapy import *
from scrapy.linkextractors import LinkExtractor
from urllib.parse import urlparse
from WebScanner.items_link import LinkItem
from pymysql import *
from scrapy.conf import settings
import re
from scrapy.crawler import CrawlerProcess


list = []



class TestSpider(Spider):
    '''根据指定的目标爬取网站的所有链接'''

    # 给爬虫命名
    name = 'TestSpider'
    # 为每个spider指定对应的pipelines
    custom_settings = {
        'ITEM_PIPELINES': {'WebScanner.pipelines_mysqldb_linktable.LinkPipeline': 300}
    }
    # 指定爬取的开始链接
    # start_urls = ["http://books.toscrape.com/"]
    # 获取目标的域名
    allow_domain = []
    # allow_domain.append(urlparse(start_urls[0]).netloc)
    # 爬取最大限制数
    max_crawl = 3000
    # 爬取的行数，即爬取到第几个链接
    linkth = 0

    # 将得到的Connection对象和Cursor对象分别赋值给self.db_conn和self.db_cur，以便之后使用。
    db_conn = connect(host='localhost', port=3306, db='webscanner', user='root', passwd='toor', charset='utf8')
    db_cur = db_conn.cursor()

    def __init__(self, *args, **kwargs):
        super(TestSpider, self).__init__(*args, **kwargs)
        # 命令行指定start_url
        self.start_urls = [kwargs.get('start_url')]
        list.append(self.start_urls[0])
        self.allow_domain.append(urlparse(self.start_urls[0]).netloc)

    def start_requests(self):
        '''重写starturl的请求'''

        # 设置cookie便于访问登录后的页面
        self.cookie = settings['COOKIES']
        yield Request(self.start_urls[0], callback=self.parse, cookies=self.cookie,dont_filter=True)

    def parse(self, response):
        # 连接数据库
        # db = conn.connsql()
        # 使用cursor()方法获取操作游标
        # cursor = db.cursor()

        # 提取开始链接的页面中 所有属于目标域的URL
        deny_parttern = '.+(delete|remove|stop|undeploy|reload|restart|' \
                        'logout|signout|logoff|signoff|exit|quit|byebye|bye-bye|clearuser|invalidate|setup|reset).+'
        links = LinkExtractor(allow_domains=self.allow_domain, deny=deny_parttern).extract_links(response)

        # 将提取的链接插入数据库
        for link in links:
            list.append(link)
            # linkitem = LinkItem()
            # linkitem['link'] = link.url
            # yield linkitem

        self.linkth = self.linkth + 1
        next_url = list[self.linkth]

        if next_url and self.linkth < self.max_crawl:

            # 如果找到下一页的URL，构造新的Request 对象
            yield Request(next_url, callback=self.parse, cookies=self.cookie,dont_filter=True)
        else:
            #探测带参数的url
            self.linkth = 0
            next_url = self.select_db(self.linkth)
            if next_url:
                yield Request(next_url, callback=self.form_parse, cookies=self.cookie, dont_filter=True)
            else:
                self.db_conn.close()


    def form_parse(self, response):

        # 根据需求转化 response.encoding
        try:
            html = response.body.decode(response.encoding)
        except:
            html = ''
        formdata = self.form_find(html)
        print(len(formdata))
        if len(formdata) > 0 and '=' not in response.url:
            linkitem = LinkItem()
            geturl = response.url+'?'
            for form in formdata:
                 geturl = geturl + form.get('name') + '=' + form.get('value') + '&'
            #去掉最后一个字符，即最后一个&删除
            linkitem['link'] = geturl[:-1]
            print('6666666666666666666666666',linkitem['link'])
            yield linkitem

        self.linkth = self.linkth + 1
        next_url = self.select_db(self.linkth)
        print(next_url)
        if next_url:
            yield Request(next_url, callback=self.form_parse, cookies=self.cookie, dont_filter=True)
        else:
            self.db_conn.close()
        return



    def form_find(self, html):
        '''在登录页面的响应中找到form表单，并根据表单属性等获取fromdata'''


        parameter_list = []
        tgtform = ''
        # 匹配form表单列
        formmatch = re.finditer('<form.*>([\s\S])*</form>', html)
        if formmatch == None:
            return None
        for form in formmatch:
            tgtform = form.group()

        inputmatch = re.finditer('<input[^>]+>', tgtform)
        if inputmatch == None:
            return parameter_list
        # 匹配form里面的所有参数和值
        for q in inputmatch:
            namematch = re.finditer('name="(?P<name>[^ ]+)"', q.group())
            if namematch == None:
                break
            else:
                for match in namematch:
                    name = match.group('name')
                valuematch = re.finditer('value="(?P<value>[^ ]+)"', q.group())
                value = ''
                if valuematch != None:
                    for match1 in valuematch:
                        value = match1.group('value')
                parameter_list.append({'name':name,'value': value})
                # formdatalist.append(parameter_list)
        print('@@@@@@@@@@@@@@@@@@@@@@@@@@@',parameter_list)
        return parameter_list

    #######################################################

    def select_db(self, linkth):
        '''查询链接'''
        sql = 'select link from t_link_tmp where id=%s'
        self.db_cur.execute(sql, linkth)
        try:
            nextlink = self.db_cur.fetchone()[0]
        except:
            nextlink = None
        return nextlink
    #############################################################


def main(url):
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })
    process.crawl(TestSpider,start_url=url)
    process.start() # the script will block here until the crawling is finished
    # scrapy.cmdline.execute(('scrapy crawl WeakpwdSpider -a start_url='+url[0]).split())  # 这就是我们在命令行中的代码

if __name__ == '__main__':
    main('http://192.168.177.161/dvwa/index.php')
