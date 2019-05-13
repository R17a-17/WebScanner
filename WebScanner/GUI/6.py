#--Created by WD
#python 3.6
#coding:utf-8

#coding = utf-8
from tkinter import *
from tkinter import StringVar
import time


class Progress(object):
    """docstring for Progress"""

    def __init__(self):
        self.root = Tk()
        self.root.geometry('245x30')
        self.root.title('进度条')

        self.var = StringVar()
        self.var.set("开始")
        self.button =  Button(self.root,textvariable = self.var,command = self.start, width = 5)
        self.button.grid(row = 0,column = 0,padx = 5)

        # 创建一个背景色为白色的矩形
        self.canvas = Canvas(self.root,bg = "white")
        # 创建一个矩形外边框（距离左边，距离顶部，矩形宽度，矩形高度），线型宽度，颜色
        self.out_line = self.canvas.create_rectangle(2,2,180,27,width = 1,outline = "black")
        self.canvas.grid(row = 0,column = 1,ipadx = 5)

        self.root.mainloop()

    def start(self):
        self.button.config(state="disable") # 设置按钮只允许点击一次
        fill_line = self.canvas.create_rectangle(2,2,0,27,width = 0,fill = "blue")

        x = 200    # 未知变量，可更改
        n = 180/x  # 180是矩形填充满的次数
        k = 100/x  # 显示值

        for i in range(x):
            n = n+180/x
            k = k+100/x
            # 以矩形的长度作为变量值更新
            self.canvas.coords(fill_line, (0, 0, n, 30))
            if k >= 100:
                self.var.set("100%")
            else:
                self.var.set(str(round(k,1))+"%")
            self.root.update()
            time.sleep(0.01)

if __name__ == '__main__':
    Progress()
