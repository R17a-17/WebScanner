#--Created by WD
#python 3.6
#coding:utf-8

import os
import subprocess

def linkspider_exec(url):
    #执行LinkSpider
    # print(os.system("cd"))#cd Spider
    cmd = "scrapy crawl LinkSpider -a start_url=" + url
    print(cmd)
    os.system(cmd)
    info = os.system(cmd)#执行LinkSpider爬取链接

    return info

if __name__ == "__main__":
    info = linkspider_exec("http://books.toscrape.com")
    print(info)