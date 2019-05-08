#--Created by WD
#python 3.6
#coding:utf-8
#class:主图形界面

from tkinter import *
from tkinter import ttk

class GuiApplication(Frame):
    '主界面：登录后的主界面。工具栏包含配置和帮助；配置控件包括目标、配置文本框，扫描、暂停、取消按钮；包括目录结构和结果显示'
    bgColor = 'black'  #背景色:黑色
    widgetColor = 'DarkMagenta' # 控件字体颜色：深洋红
    fontColor = 'DarkGreen'  # 内容字体颜色：暗绿色
    width = 810 #窗口宽度
    height = 670 #窗口高度
    title = 'Web Vulnerability Scanner'

    def __init__(self, master=None):
        super().__init__(master)
        self.setGeometry()
        self.setBg()
        self.setTitle()
        self.setResizable()
        self.setMenu()
        self.setTgtLabel()
        self.setTgtEntry()
        self.setConfLabel()
        self.setConfCombobox()
        self.setButton()
        self.setFrame()
        self.createWidgets()

    def setTitle(self):
        '标题'
        self.master.title(self.title)

    def setGeometry(self):
        '设置初始界面的大小和位置'
        #设置初始大小、位置
        self.master.geometry("%dx%d+%d+%d" % (
        self.width, self.height, (self.master.winfo_screenwidth() - self.width) / 2,
        (self.master.winfo_screenheight() - self.height) / 2 - 60))
        self.master.rowconfigure(0, weight=1)
        #设置顶级窗体的行列权重，否则子组件的拉伸不会填充整个窗体
        self.master.columnconfigure(0, weight=1)

    def setResizable(self):
        '设置窗口不能变大'
        self.master.resizable(width=True, height=True)

    def setBg(self):
        '设置背景色'
        self['bg']=self.bgColor

    def setMenu(self):
        '设置菜单栏'
        menubar = Menu(self)
        for each in ['配置(P)', '帮助(H)']:
            menubar.add_command(label=each)
        self.master['menu'] = menubar

    def setTgtLabel(self):
        '设置目标标签'
        tgtLabel = Label(text='目标：').grid(row=0, column=0, sticky=N + W)

    def setTgtEntry(self):
        '设置目标填写的文本框'
        tgtEntry = Entry(self.master, bd=3, width=20).grid(row=0, column=30,sticky=N + W)

    def setConfLabel(self):
        '设置配置标签'
        confLabel = Label(text='配置：').grid(row=0, column=100, sticky=N + W)

    def setConfCombobox(self):
        '设置配置的下拉列表'
        confCombobox = ttk.Combobox(self)
        comvalue = StringVar()  # 窗体自带的文本，新建一个值
        comboxlist = ttk.Combobox(self.master, textvariable = comvalue,width = 20,state = 'readonly')  # 初始化
        confList = ('综合扫描', 'XSS', 'SQL注入', 'CLRF')
        comboxlist["values"] = confList
        comboxlist.current(0)  # 选择第一个
        # comboxlist.bind("<<ComboboxSelected>>", go)  # 绑定事件,(下拉列表框被选中时，绑定go()函数)
        comboxlist.grid(row=0, column=130,sticky=N + W)

    def createWidgets(self):
        '创建组件'
        # menubar = Menu(root)

    def setButton(self):

        '扫描取消按钮'
        scanButton = Button(self.master, text='扫描', command="print('hi')").grid(row=0, column=200,sticky=E+N)
        cancelButton = Button(self.master, text='取消', command="print('hi')").grid(row=0, column=250,sticky=E+N)

    def setFrame(self):
        '左侧目录结构框架'
        dirFrame = Frame(self.master,background = self.bgColor, width = 400,height = 500).grid(row=5,column=0)
        mainFrame = Frame(self.master,background = self.fontColor, width = 400,height = 500).grid(row=5,column=20)

app = GuiApplication(master=Tk())
app.mainloop() #进入消息循环
