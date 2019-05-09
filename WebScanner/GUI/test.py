# from tkinter import *
# import tkinter.messagebox as messagebox
#
#
# class A:
#     """
#     使用StringVar() 和 textvariable
#     对Button进行绑定
#     实现Button对数据进行操作
#     解决Button传参问题
#     StringVar()的数需要使用.get()获取值
#     """
#     def __init__(self, master):
#         self.root = Frame(master)
#         self.num1 = StringVar()  # 第一个数字
#         self.num2 = StringVar()  # 第一个数字
#         self.createpage()
#
#     def createpage(self):
#         self.root.pack()
#         Label(self.root, text='num1').grid(row=0, column=0, stick=W, pady=10)
#         # textvariable和StringVar的num1绑定
#         Entry(self.root, textvariable=self.num1).grid(row=0, column=1, stick=E)
#         Label(self.root, text='num2').grid(row=1, column=0, stick=W, pady=10)
#         # textvariable和StringVar的num2绑定
#         Entry(self.root, textvariable=self.num2).grid(row=1, column=1, stick=E)
#         # Button传递参数
#         Button(
#             self.root, text='加', command=self.btn_def
#         ).grid(row=2, column=0, stick=W)
#         Button(self.root, text='减').grid(row=2, column=1, stick=E)
#         Label(self.root, text='说明').grid(row=3, column=0, stick=W, pady=10)
#         Label(self.root, text='只写了加法(请输入简单数字测试button传参)').grid(
#             row=3, column=1, stick=E
#         )
#
#     def btn_def(self):
#         # 使用.get()获取值
#         num = int(self.num1.get()) + int(self.num2.get())
#         messagebox.showinfo('结果', '%d' % num)
#
#
# if __name__ == '__main__':
#     root = Tk()
#     root.title('Demo2')
#     root.geometry('400x150')
#     A(root)
#     root.mainloop()

# # --Created by WD
# # coding:utf-8
#
# from tkinter import *
# from tkinter import ttk
#
# top = Tk()
# top.rowconfigure(0,weight=1)
# top.columnconfigure(0,weight=1)
# top.title('ttttt')
# # top['bg']='black'
# top.geometry('500x500+250+200')
# top.resizable(width=True, height=True)
# menubar = Menu(top)
# for each in ['文件','视图','编辑','关于']:
#     menubar.add_command(label=each)
# top['menu']=menubar
#
# tgtLabel = Label(text='目标：').grid(row = 0,column = 0, sticky = N + W)
#
# tgtEntry = Entry(top,bd=3,width=30).grid(row=0,column=30)
#
# confLabel = Label(text = '配置：').grid(row = 0,column = 100,sticky = N+W)
#
# confCombobox = ttk.Combobox(top)
# comvalue = StringVar()  # 窗体自带的文本，新建一个值
# comboxlist = ttk.Combobox(top, textvariable=comvalue, state='readonly')  # 初始化
# confList = ('综合扫描','xss','SQL注入','CLRF')
# comboxlist["values"] = confList
# comboxlist.current(0)  # 选择第一个
# # comboxlist.bind("<<ComboboxSelected>>", go)  # 绑定事件,(下拉列表框被选中时，绑定go()函数)
# comboxlist.grid(row=0,column=130)
#
# scanButton = Button(top,text = '扫描',command="print('hi')").grid(row=0,column=200)
# cancelButton = Button(top,text = '取消',command="print('hi')").grid(row=0,column=200)
#
# # dirFrame = Frame(bg='black',width = 400,height = 500).grid(row=4,column=0)
# # Label(text='hfdsjhjdsfh',bg='black').grid(row=0,column=0, sticky= N + E + W + S)
#
# top.mainloop()

# !/usr/bin/env python3
# coding:utf-8

import tkinter as tk
import tkinter.font as tkFont
import tkinter.messagebox
import tkinter.ttk as ttk


class MForm(tk.Frame):
    '''继承自Frame类，master为Tk类顶级窗体（带标题栏、最大、最小、关闭按钮）'''

    def __init__(self, master=None):
        super().__init__(master)
        self.initComponent(master)
    def initComponent(self, master):
        '''初始化GUI组件'''
        # 设置顶级窗体的行列权重，否则子组件的拉伸不会填充整个窗体
        master.rowconfigure(0, weight=1)
        master.columnconfigure(0, weight=1)
        self.ft = tkFont.Font(family='微软雅黑', size=12, weight='bold')  # 创建字体
        self.initMenu(master)  # 为顶级窗体添加菜单
        # 设置继承类MWindow的grid布局位置，并向四个方向拉伸以填充顶级窗体
        self.grid(row=0, column=0, sticky=tk.NSEW)
        # 设置继承类MWindow的行列权重，保证内建子组件会拉伸填充
        self.rowconfigure(0, weight=1);
        self.columnconfigure(0, weight=1)
        self.panewin = ttk.Panedwindow(self, orient=tk.HORIZONTAL)  # 添加水平方向的推拉窗组件
        self.panewin.grid(row=0, column=0, sticky=tk.NSEW)  # 向四个方向拉伸填满MWindow帧
        self.frm_left = ttk.Frame(self.panewin, relief=tk.SUNKEN, padding=0)  # 左侧Frame帧用于放置播放列
        self.frm_left.grid(row=0, column=0, sticky=tk.NS);  # 左侧Frame帧拉伸填充
        self.panewin.add(self.frm_left, weight=1)  # 将左侧Frame帧添加到推拉窗控件，左侧权重1
        self.initPlayList()  # 添加树状视图
        self.frm_right = ttk.Frame(self.panewin, relief=tk.SUNKEN)  # 右侧Frame帧用于放置视频区域和控制按钮
        self.frm_right.grid(row=0, column=0, sticky=tk.NSEW)  # 右侧Frame帧四个方向拉伸
        self.frm_right.columnconfigure(0, weight=1);  # 右侧Frame帧两行一列，配置列的权重
        self.frm_right.rowconfigure(0, weight=8);  # 右侧Frame帧两行的权重8:1
        self.frm_right.rowconfigure(1, weight=1)
        self.panewin.add(self.frm_right, weight=50)  # 将右侧Frame帧添加到推拉窗控件,右侧权重10
        s = ttk.Style();
        s.configure('www.TFrame', background='black')  # 视频区Frame帧添加样式
        # 右侧Frame帧第一行添加视频区Frame
        self.frm_vedio = ttk.Frame(self.frm_right, relief=tk.RIDGE, style='www.TFrame')
        self.frm_vedio.grid(row=0, column=0, sticky=tk.NSEW)
        # 右侧Frame帧第二行添加控制按钮
        self.frm_control = ttk.Frame(self.frm_right, relief=tk.RAISED)  # 四个方向拉伸
        self.frm_control.grid(row=1, column=0, sticky=tk.NSEW)
        self.initCtrl()  # 添加滑块及按钮

    def initMenu(self, master):
        '''初始化菜单'''
        mbar = tk.Menu(master)  # 定义顶级菜单实例
        fmenu = tk.Menu(mbar, tearoff=False)  # 在顶级菜单下创建菜单项
        mbar.add_cascade(label=' 文件 ', menu=fmenu, font=('Times', 20, 'bold'))  # 添加子菜单
        fmenu.add_command(label="打开", command=self.menu_click_event)
        fmenu.add_command(label="保存", command=self.menu_click_event)
        fmenu.add_separator()  # 添加分割线
        fmenu.add_command(label="退出", command=master.quit())

        etmenu = tk.Menu(mbar, tearoff=False)
        mbar.add_cascade(label=' 编辑 ', menu=etmenu)
        for each in ['复制', '剪切', '合并']:
            etmenu.add_command(label=each, command=self.menu_click_event)
        master.config(menu=mbar)  # 将顶级菜单注册到窗体

    def menu_click_event(self):
        '''菜单事件'''
        pass


    def initPlayList(self):
        '''初始化树状视图'''
        self.frm_left.rowconfigure(0, weight=1)  # 左侧Frame帧行列权重配置以便子元素填充布局
        self.frm_left.columnconfigure(0, weight=1)  # 左侧Frame帧中添加树状视图
        tree = ttk.Treeview(self.frm_left, selectmode='browse', show='tree', padding=[0, 0, 0, 0])
        tree.grid(row=0, column=0, sticky=tk.NSEW)  # 树状视图填充左侧Frame帧
        tree.column('#0', width=150)  # 设置图标列的宽度，视图的宽度由所有列的宽决定
        # 一级节点parent='',index=第几个节点,iid=None则自动生成并返回，text为图标右侧显示文字
        # values值与columns给定的值对应
        tr_root = tree.insert("", 0, None, open=True, text='播放列表')  # 树视图添加根节点
        node1 = tree.insert(tr_root, 0, None, open=True, text='本地文件')  # 根节点下添加一级节点
        node11 = tree.insert(node1, 0, None, text='文件1')  # 添加二级节点
        node12 = tree.insert(node1, 1, None, text='文件2')  # 添加二级节点
        node2 = tree.insert(tr_root, 1, None, open=True, text='网络文件')  # 根节点下添加一级节点
        node21 = tree.insert(node2, 0, None, text='文件1')  # 添加二级节点
        node22 = tree.insert(node2, 1, None, text='文件2')  # 添加二级节点

    def initCtrl(self):
        '''初始化控制滑块及按钮'''


        self.frm_control.columnconfigure(0, weight=1);  # 配置控制区Frame各行列的权重
        self.frm_control.rowconfigure(0, weight=1);  # 第一行添加滑动块
        self.frm_control.rowconfigure(1, weight=1);  # 第二行添加按钮
        slid = ttk.Scale(self.frm_control, from_=0, to=900, command=self.sliderValueChanged)
        slid.grid(row=0, column=0, sticky=tk.EW, padx=2)  # 滑动块水平方向拉伸

        frm_but = ttk.Frame(self.frm_control, padding=2)  # 控制区第二行放置按钮及标签
        frm_but.grid(row=1, column=0, sticky=tk.EW)
        self.lab_curr = ttk.Label(frm_but, text="00:00:00", font=self.ft)  # 标签显示当前时间
        lab_max = ttk.Label(frm_but, text="00:00:00", font=self.ft)  # 标签显示视频长度
        self.lab_curr.grid(row=0, column=0, sticky=tk.W, padx=3)
        lab_max.grid(row=0, column=13, sticky=tk.E, padx=3)
        i = 4
        for but in ['播放', '暂停', '快进', '快退', '静音']:
            ttk.Button(frm_but, text=but).grid(row=0, column=i)
            i += 1
        for i in range(14):  # 为每列添加权重值以便水平拉伸
            frm_but.columnconfigure(i, weight=1)


    def sliderValueChanged(self, val):
        '''slider改变滑块值的事件'''
        # tkinter.messagebox.showinfo("Message", "message")
        flt = float(val);
        strs = str('%.1f' % flt)
        self.lab_curr.config(text=strs)

if (__name__ == '__main__'):
    root = tk.Tk()
    root.geometry('800x480+200+100')
    root.title('Media Player')
    # root.option_add("*Font", "宋体")
    root.minsize(800, 480)
    app = MForm(root)
    root.mainloop()