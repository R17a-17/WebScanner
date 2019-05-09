#--Created by WD
#python 3.6
#coding:utf-8

import time
import subprocess
import locale
import codecs

popen = subprocess.Popen(['ping', 'www.baidu.com', '-n', '3'], stdout = subprocess.PIPE)

while True:
    print(popen.stdout.readline())