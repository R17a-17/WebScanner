#--Created by WD
#python 3.6
#coding:utf-8

# !/usr/bin/python
# -*- coding: UTF-8 -*-

import tkinter

# 创建一个矩形，指定画布的颜色为白色
from tkinter import *

root = Tk()
# 创建一个Canvas，设置其背景色为白色
frame = tkinter.Frame(root)
frame.pack()
cv = Canvas(frame, bg='white')
# 创建一个矩形，坐标为(10,10,110,110)
cv.create_rectangle(10, 10, 110, 110)
cv.pack()

root.mainloop()
