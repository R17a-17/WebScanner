#--Created by WD
#python 3.6
#coding:utf-8

from scrapy import *

class VulnDetectSpider(Spider):
    '''漏洞探测：对每个URL进行测试，包括xss、sqli、Weakpassword、CSRF'''
    #爬虫命名
    name = 'VulnDetectSpider'

    def parse(self):
        pass