#--Created by WD
#python 3.6
#coding:utf-8

'''
LinkSpider item
'''


from scrapy import Item, Field
    # define the fields for your item here like:


class LinkItem(Item):
    '''define the fields for your item'''
    link = Field()