#--Created by WD
#python 3.6
#coding:utf-8

#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import subprocess


# 与在命令窗口执行显示效果相同，如有彩色输出可保留，但不能返回结果
def run(command):
    subprocess.call(command, shell=True)


# 实时输出但不可显示彩色，可以返回结果
def sh(command, print_msg=True):
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    lines = []
    for line in iter(p.stdout.readline, b''):
        line = line.rstrip().decode('utf8')
        if print_msg:
            print(">>>", line)
        lines.append(line)
    return lines


print('run():')
run("ping www.baidu.com")
print('\n\nsh():')
run("ping www.baidu.com")
