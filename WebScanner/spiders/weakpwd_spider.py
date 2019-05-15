#--Created by WD
#python 3.6
#coding:utf-8

from scrapy import *
from pymysql import *
import re
import random
import requests
import json
from WebScanner.Vulnerability_policy_Library.WeakPd.pass_list import pass_list
from scrapy.crawler import CrawlerProcess
import scrapy.cmdline

class Weakpwd_Spider(Spider):
    '''弱口令漏洞检测'''

    name = 'WeakpwdSpider'

    def __init__(self, *args, **kwargs):
        super(Weakpwd_Spider, self).__init__(*args, **kwargs)
        #命令行指定start_url
        self.start_urls =  [kwargs.get('start_url')]
        self.url = self.start_urls[0]
        self.passth = 0
        self.username = None
        self.password = None
        self.pass_list = pass_list
        self.cookie = ''

    def start_requests(self):
        '''重写starturl的请求'''
        # 开始url
        print('>>>WebScanner正在扫描弱口令漏洞...')
        self.start_urls = []
        self.start_urls.append(self.url)
        yield Request(self.start_urls[0], callback=self.parse)


    def parse(self, response):

        '''从字典列表中获取一个密码'''
        self.username = 'admin'
        self.password = self.pass_list[self.passth]
        #根据表单属性等获取fromdata
        formlist = self.form_find(str(response.body))
        formdata = {
            formlist[2]:self.username,
            formlist[4]:self.password,
            formlist[6]:formlist[7],
        }
        self.formdata = formdata
        return FormRequest.from_response(
            response,
            method = 'POST',
            formdata= formdata,
            callback=self.after_login,
            dont_filter=True,#由于暴力破解针对同一个url，这里一定要设置，否则重复链接不会进行下一步爬取
            meta={'cookiejar': True}
        )


    def after_login(self, response):
        '''check login succeed before going on'''
        if response.url == self.start_urls[0]:
            print(r'>>>登录失败')
            self.passth = self.passth + 1
            yield Request(self.start_urls[0], callback=self.parse, dont_filter = True)
        else:
            print('>>>登录成功!!!用户名:', self.username, ',密码:', self.password)
            string = 'Weak Password:the username is ' + self.username + 'and the password:'+self.password
            print(string)
            # # dumps 将数据转换成字符串
            # json_str = json.dumps(self.formdata)
            # print(json_str)
            # print(type(json_str))
            # 将得到的Connection对象和Cursor对象分别赋值给self.db_conn和self.db_cur，以便之后使用。
            db_conn = connect(host='localhost', port=3306, db='webscanner', user='root', passwd='toor', charset='utf8')
            db_cur = db_conn.cursor()
            values = (
                self.start_urls[0],
                string
            )
            sql = 'INSERT INTO t_vulninfo(vulnurl, vulntype) VALUES (%s,%s)'
            # sql = 'INSERT INTO t_link_tmp(link) SELECT %s FROM DUAL WHERE NOT EXISTS(SELECT link from t_link_tmp where link = %s)'
            db_cur.execute(sql,values)
            db_conn.commit()
            db_conn.close()


        return


    def form_find(self, html):
        '''在登录页面的响应中找到form表单，并根据表单属性等获取fromdata'''
        action = None
        method = None
        username_parameter = None
        username_value = None
        password_parameter = None
        password_value = None
        loginbutton_parameter = None
        loginbutton_value = None
        #匹配form表单列表
        for form in re.finditer(r'<form.*>([\s\S])*</form>', html):
            if 'username' in form.group() or 'password' in form.group() or 'pass' in form.group() or 'pwd' in form.group() or 'accout' in form.group():
                tgtform = form.group()

        #匹配form里面的所有参数和值
        parameter_list = []
        for p in re.finditer(r'(?P<parameter>[\w]+)="(?P<value>[^ ]+)"( |>)', tgtform):
            parameter_list.append({'parameter':p.group('parameter'),'value':p.group('value')})
            #匹配action
            if p.group('parameter') == 'action':
                action = p.group('value')
            #匹配http方法
            if p.group('parameter') == 'method':
                method = p.group('value')

        #匹配input里面的所有参数和值
        for q in re.finditer(r'<input( )+(((?P<parameter>[\w]*)="(?P<value>[^ ]+)"( )?))+>', form.group()):
            if 'name="username"' in q.group():
                username_parameter = 'username'
                username_value = q.group('value')
            if 'name="password"' in q.group():
                password_parameter = 'password'
                password_value = q.group('value')
            if 'button' in q.group() or 'submit' in q.group() or 'login' in q.group().lower():
                loginbutton_parameter = q.group('value')
                if 'value' in q.group().lower():
                    for r in re.finditer(r'value="(?P<loginvalue>[^ ]+)"( )?', q.group()):
                        loginbutton_value = 'login'

        return action, method, username_parameter,username_value, password_parameter,password_value, loginbutton_parameter,loginbutton_value

def main(url):
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })
    process.crawl(Weakpwd_Spider,start_url=url)
    process.start() # the script will block here until the crawling is finished
    # scrapy.cmdline.execute(('scrapy crawl WeakpwdSpider -a start_url='+url[0]).split())  # 这就是我们在命令行中的代码

if __name__ == '__main__':
    pass
    # main(url)