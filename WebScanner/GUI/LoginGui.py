#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os, sys
 #Python 3.x
from tkinter import *
from tkinter.font import Font
from tkinter.ttk import *
from tkinter.messagebox import *
#import tkinter.filedialog as tkFileDialog
 #import tkinter.simpledialog as tkSimpleDialog    #askstring()

class Application_ui(Frame):
    #这个类仅实现界面生成功能，具体事件处理代码在子类Application中。
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master.title('Form1')
        self.master.geometry('389x339')
        self.createWidgets()

    def createWidgets(self):
        self.top = self.winfo_toplevel()

        self.style = Style()

        #添加NoteBook并显示
        self.tabNote = Notebook(self.top)
        self.tabNote.grid(row=0, column=0, sticky=NW)

        # 添加一个标签页：扫描进度
        self.tabScanPage = Frame(self.tabNote)
        self.Tab1Lbl = Label(self.tabScanPage, text='Please add widgets in code.')
        self.Tab1Lbl.grid(row=0,column=0,sticky=NW)
        e = StringVar
        self.Tab1Entry1 =Entry(self.tabScanPage,textvariable = e)
        e.set('hhh')
        self.Tab1Entry1.grid(row=0,column=1,sticky=NW)

        self.tabNote.add(self.tabScanPage, text='扫描进度')

        #添加一个标签页：风险视图
        self.tabResultPage = Frame(self.tabNote)
        self.tabNote.add(self.tabResultPage, text='风险视图')

        #添加一个标签页：扫描结果
        self.tabResultPage = Frame(self.tabNote)
        self.tabNote.add(self.tabResultPage, text='扫描结果')

        # self.TabNote = Notebook(self.top)
        # self.TabNote.place(relx=0.062, rely=0.071, relwidth=0.887, relheight=0.876)
        #
        # self.Tab1 = Frame(self.TabNote)
        # self.Tab1Lbl = Label(self.Tab1, text='Please add widgets in code.')
        # self.Tab1Lbl.place(relx=0.1,rely=0.5)
        # self.TabNote.add(self.Tab1, text='我的快玩')
        #
        # self.Tab2 = Frame(self.TabNote)
        # self.Tab2Lbl = Label(self.Tab2, text='Please add widgets in code.')
        # self.Tab2Lbl.place(relx=0.1,rely=0.5)
        # self.TabNote.add(self.Tab2, text='找游戏')
        #
        #
        # # 添加一个标签页：扫描进度
        # self.tabScanPage = Frame(self.TabNote)
        # self.Tab3Lbl =  Label(self.tabScanPage, text='Please add widgets in code.')
        # self.Tab3Lbl.grid(row=0,column=0,sticky= NW)
        # self.TabNote.add(self.tabScanPage, text='扫描进度')


class Application(Application_ui):
    #这个类实现具体的事件处理回调函数。界面生成代码在Application_ui中。
    def __init__(self, master=None):
        Application_ui.__init__(self, master)

if __name__ == "__main__":
    top = Tk()
    Application(top).mainloop()



