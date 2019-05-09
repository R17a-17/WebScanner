#--Created by WD
#python 3.6
#coding:utf-8
import subprocess
import sys


popen = subprocess.Popen(['scrapy', 'crawl', 'WeakpwdSpider'], stdout = subprocess.PIPE)

while True:
    if popen.stdout.readline() == b'':
        break
    print(popen.stdout.readline())
