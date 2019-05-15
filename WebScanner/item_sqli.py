#--Created by WD
#python 3.6
#coding:utf-8

'''
XssSpider item
'''


from scrapy import Item, Field
    # define the fields for your item here like:


class SqliItem(Item):
    '''define the fields for your item'''
    vulnurl = Field()#存在漏洞的link
    vulntype = Field()