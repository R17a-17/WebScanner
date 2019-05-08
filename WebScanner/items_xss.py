#--Created by WD
#python 3.6
#coding:utf-8

'''
XssSpider item
'''


from scrapy import Item, Field
    # define the fields for your item here like:


class XssItem(Item):
    '''define the fields for your item'''
    vulnurl = Field()#存在漏洞的link
    vulntype = Field()#漏洞类型
    origin_request = Field()#原始请求
    origin_response = Field()#原始响应
    detect_request = Field()#测试请求
    detect_response = Field()#测试响应