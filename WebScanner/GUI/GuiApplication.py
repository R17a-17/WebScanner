# --Created by WD
# python 3.6
# coding:utf-8

#————————————————————————
#外部包导入
import tkinter as tk
import tkinter.font as tkFont
import tkinter.ttk as ttk
from tkinter import messagebox
import subprocess
import threading
#-----------------------------------------------
#内部包导入
from WebScanner.GUI import Verify
from WebScanner.GUI import SiteFileTree
from WebScanner.GUI import Histogram
from WebScanner.GUI import PieChart
from WebScanner.Mysqldb import GetVuln
#--------------------------------------------------

class MForm(tk.Frame):
    '''继承自Frame类，master为Tk类顶级窗体（带标题栏、最大、最小、关闭按钮）'''

    width = 810 #窗口宽度
    height = 680 #窗口高度
    title = 'Web Vulnerability Scanner'
    iconPath = '../img/tkicon.ico'


    def __init__(self, master=None):
        super().__init__(master)
        self.initComponent(master)
        self.info = []
        # 大小不可变（最大化按钮不可用）
        root.resizable(False, False)
        self.cmd = ''



    def initComponent(self, master):
        '''初始化GUI组件'''
        #设置顶级窗口的初始大小和位置，位置居中
        self.master.geometry("%dx%d+%d+%d" % (
        self.width, self.height, (self.master.winfo_screenwidth() - self.width) / 2,
        (self.master.winfo_screenheight() - self.height) / 2 - 60))
        #设置顶级窗口的标题
        self.master.title(self.title)
        # 设置顶级窗体的行列权重，否则子组件的拉伸不会填充整个窗体
        master.rowconfigure(0, weight=1)
        master.columnconfigure(0, weight=1)
        # 创建字体 
        self.ft = tkFont.Font(family='微软雅黑', size=12, weight='bold')
        #为顶级窗体添加菜单项
        self.initMenu(master)
        self.master.iconbitmap(self.iconPath)

        # 设置继承类MWindow的grid布局位置，并向四个方向拉伸以填充顶级窗体，NSEW代表北南东西四个方向
        self.grid(row=0, column=0, sticky=tk.NSEW)
        # 设置继承类MWindow的行列权重，保证内建子组件会拉伸填充
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        # 添加垂直方向的面板
        self.paneTop = ttk.Panedwindow(self, orient=tk.VERTICAL)
        self.paneTop.grid(row=0, column=0, sticky=tk.NSEW)  # 向四个方向拉伸填满MWindow帧
        #面板的第一行和第二行权重为1:9
        self.paneTop.rowconfigure(0,weight=1)
        self.paneTop.rowconfigure(1, weight=10)
        #面板第一列权重为1
        self.paneTop.columnconfigure(0,weight=1)

        #添加上面的面板
        self.paneUp = ttk.Panedwindow(self.paneTop, orient=tk.HORIZONTAL)
        self.paneUp.grid(row=0, column=0, sticky=tk.NSEW)  # 向四个方向拉伸填满MWindow帧
        #上面Frame帧用于设置目标等
        self.frm_up = ttk.Frame(self.paneUp, relief=tk.SUNKEN, padding=0)
        # Frame帧拉伸东西填充
        self.frm_up.grid(row=0, column=0,sticky = tk.NSEW)
        # 将Frame帧添加到推拉窗控件，权重1
        self.paneUp.add(self.frm_up)
        self.initSetting()

        # 添加下面的面板
        self.panewin = ttk.Panedwindow(self.paneTop, orient=tk.HORIZONTAL)
        self.panewin.grid(row=1, column=0, sticky=tk.NSEW)  # 向四个方向拉伸填满MWindow帧
        self.panewin.rowconfigure(0,weight=1)
        self.panewin.columnconfigure(0,weight=1)
        self.panewin.columnconfigure(1,weight=1)

        self.frm_left = ttk.Frame(self.panewin, relief=tk.SUNKEN, padding=0)  # 左侧Frame帧用于放置网站目录
        self.frm_left.grid(row=0, column=0, sticky=tk.NS)  # 左侧Frame帧拉伸填充
        self.panewin.add(self.frm_left) # 将左侧Frame帧添加到推拉窗控件，左侧权重1
        self.initDirList()  # 添加网站目录树状视图

        self.frm_right = ttk.Frame(self.panewin, relief=tk.SUNKEN)  # 右侧Frame帧用于放置扫描结果
        self.frm_right.grid(row=0, column=1, sticky=tk.NSEW)  # 右侧Frame帧四个方向拉伸
        self.panewin.add(self.frm_right)# 将右侧Frame帧添加到面板
        self.initCtrl()#初始化右侧结果显示界面


    def initMenu(self, master):
        '''初始化菜单'''
        #在顶级菜单下创建菜单项
        menubar = tk.Menu(self)
        # 在顶级菜单下创建菜单项:帮助
        hmenu =tk.Menu (menubar, tearoff=False)
        menubar.add_cascade(label='帮助(H)', menu=hmenu)  # 添加子菜单
        hmenu.add_command(label="使用方法", command=lambda :self.usemenu())
        hmenu.add_command(label="关于", command=lambda :self.aboutmenu())
        self.master['menu'] = menubar

    def initSetting(self):
        '''上面帧的配置：初始化目标、配置等控件'''
        self.frm_up.rowconfigure(0, weight=1)# 左侧Frame帧第一行权重配置以便子元素填充布局
        self.frm_up.rowconfigure(1, weight=1)# 左侧Frame帧第二行权重配置以便子元素填充布局                  

        #设置目标标签
        tgtLabel = tk.Label(self.frm_up,text=' 目标：').grid(row=0, column=0,sticky = tk.NSEW, padx=3, pady=3)
        #设置目标填写的文本框
        tgt = tk.StringVar()
        tgt.set('')
        self.tgtEntry = tk.Entry(self.frm_up, bd=3,width=40, textvariable = tgt)
        self.tgtEntry.grid(row=0, column=1, sticky=tk.W)

        #设置配置标签
        confLabel = tk.Label(self.frm_up,text='配置：').grid(row=0, column=2, sticky=tk.W,padx=3,pady=3)
        #'设置配置的下拉列表'
        comvalue = tk.StringVar()  # 窗体自带的文本，新建一个值
        self.comboxlist = ttk.Combobox(self.frm_up, textvariable=comvalue, state='readonly', width=40)  # 初始化
        # confList = ('综合扫描', 'XSS', 'SQL注入', 'CLRF', '弱口令')
        # self.comboxlist["values"] = confList
        self.comboxlist["value"] = ('综合扫描', 'XSS', 'SQL注入', 'CRLF', '弱口令')
        self.comboxlist.current(newindex=0)  # 选择第一个
        # self.comboxlist.bind("<<ComboboxSelected>>", self.combox)  # 绑定事件,(下拉列表框被选中时，绑定响应函数)
        self.comboxlist.grid(row=0, column=3, sticky=tk.W)

        #添加扫描、获取结果按钮
        self.scanButton = tk.Button(self.frm_up, text='扫描', command=lambda:self.detect_exec())
        self.scanButton.grid(row=0, column=4, sticky=tk.W,padx=6,pady=6)
        self.GetResultButton = tk.Button(self.frm_up, text='获取结果', command=lambda:self.update_result())
        self.GetResultButton.grid(row=0, column=5, sticky=tk.E,padx=6,pady=6)
        # self.GetResultButton.config(state=tk.DISABLED)
        #登录配置
        # loginLabel = tk.Labe(self.frm_up,text=' 登录：').grid(row=1, column=0,sticky = tk.W,padx=3)

        #设置命令标签、文本框
        cmdLabel = tk.Label(self.frm_up,text=' 命令：').grid(row=1, column=0,sticky = tk.W,padx=3)
        #设置命令的文本框
        self.cmdvalue = tk.StringVar()
        self.cmdvalue.set('')
        self.cmdEntry = tk.Entry(self.frm_up, bd=3,width=105, state='readonly', textvariable = self.cmdvalue)
        self.cmdEntry.grid(row=1, column=1, columnspan=5,sticky=tk.W)


    def initDirList(self):
        '''初始化目录树状视图'''
        #左侧Frame帧行列权重配置以便子元素填充布局
        self.frm_left.rowconfigure(0, weight=1)
        self.frm_left.columnconfigure(0, weight=1)

        #添加NoteBook并显示
        self.FileNote = ttk.Notebook(self.frm_left)
        self.FileNote.grid(row=0, column=0,sticky=tk.NSEW)

        # 添加一个标签页：网站目录
        self.tabFilePage = tk.Frame(self.FileNote,bg="WhiteSmoke")
        self.tabFilePage.rowconfigure(0, weight=1)
        self.tabFilePage.columnconfigure(0, weight=1)
        self.FileNote.add(self.tabFilePage, text='网站目录')

        # #添加一个树状视图的目录列表
        self.tree = ttk.Treeview(self.tabFilePage, selectmode='browse', show='tree', padding=[0, 0, 0, 0])
        self.tree.grid(row=0, column=0, sticky=tk.NSEW,padx=10,pady=10) # 树状视图填充左侧Frame帧
        self.tree.column('#0', width=150)# 设置图标列的宽度，视图的宽度由所有列的宽决定
        # 一级节点parent='',index=第几个节点,iid=None则自动生成并返回，text为图标右侧显示文字
        # values值与columns给定的值对应
        # self.tr_root = self.tree.insert("", 0, '网站目录', open=True, text='网站目录')  # 树视图添加根节点
        # node1 = self.tree.insert(self.tr_root, 0, None, open=False, text='本地文件')  # 根节点下添加一级节点
        # node11 = self.tree.insert(node1, 0, None, text='文件1')# 添加二级节点
        # node12 = self.tree.insert(node1, 1, None, text='文件2')# 添加二级节点


    def initCtrl(self):
        '''右侧frame结果显示模块'''
        self.frm_right.rowconfigure(0, weight=1)
        self.frm_right.columnconfigure(0, weight=1)

        #添加NoteBook并显示
        self.tabNote = ttk.Notebook(self.frm_right)
        self.tabNote.grid(row=0, column=0,sticky=tk.NSEW)

        # 添加一个标签页：扫描结果
        self.tabScanPage = ttk.Frame(self.tabNote,)
        self.tabScanPage.rowconfigure(0, weight=1)
        self.tabScanPage.columnconfigure(0, weight=1)
        self.tabScanPage.rowconfigure(1, weight=1)
        self.tabScanPage.columnconfigure(1, weight=1)
        self.tabNote.add(self.tabScanPage, text='扫描结果')

        #添加result列表
        self.ScanResultlist = tk.Frame(self.tabScanPage,bg='WhiteSmoke')
        self.ScanResultlist.rowconfigure(0, weight=1)
        self.ScanResultlist.columnconfigure(0, weight=1)
        self.ScanResultlist.grid(row=0, column=0, rowspan=2,sticky=tk.NSEW)
        # self.ScanProcessbar = Processbar.main(self.ScanResultlist)


        self.Resultlist = tk.Text(self.ScanResultlist,bg='white')
        self.Resultlist.grid(row=0,column=0,sticky=tk.NSEW,padx=10,pady=10)

        #添加图像显示
        self.ScanGraphView = ttk.Frame(self.tabScanPage)
        self.ScanGraphView.grid(row=0, column=1, sticky=tk.NSEW)
        #添加柱状图部分初始显示所有的漏洞都是0
        # self.Histogram = Histogram.main(self.ScanGraphView,(0,0,0,0,0))
        # #添加饼图部分,初始显示每种类型漏洞都为0，所以比例都一样
        # self.PieChart = PieChart.main(self.ScanGraphView,[25,25,25,25])




    def aboutmenu(self):
        '''菜单事件'''
        messagebox.showinfo(title='关于WebScanner',message = '版本号：V1.0，作者：吴丹\n\r用于扫描目标网站是否存在XSS、SQLi、暴力破解等漏洞')

    def usemenu(self):
        messagebox.showinfo(title='使用方法', message= 'WebScanner提供两种使用方法：命令行和交界面\n\r在使用交互界面时，请正确输入目标网站的url和扫描方法！')


    def detect_exec(self):
        # 命令行执行WeakpwdSpider，供GUI、CMD调用
        self.scanButton.config(state=tk.DISABLED)
        self.cmd = ''
        if Verify.Verify_tgt(self.tgtEntry.get()):
            messagebox.showwarning(title='警告',message='输入的目标url无效！请重新输入')
        else:
            self.Resultlist.insert(tk.END, "开启WebScanner...\n")
            if self.comboxlist.get() == 'XSS':
                self.cmd = 'scrapy crawl XssSpider'
            elif self.comboxlist.get() == 'SQL注入':
                self.cmd = 'scrapy crawl SqliSpider'
            elif self.comboxlist.get() == 'CRLF':
                self.cmd = 'scrapy crawl CRLF'
            elif self.comboxlist.get() == '弱口令':
                self.cmd = 'scrapy crawl WeakpwdSpider'
            elif self.comboxlist.get() == '综合扫描':
                self.cmd = 'scrapy crawl VulndetectSpider'
            self.cmdvalue.set(self.cmd + ' -a start_url='+ self.tgtEntry.get())
            print(self.cmd)

        self.scanButton.config(state=tk.NORMAL)


    def insertTreeNode(self):
        '''向网站列表插入子节点生成树'''
        SiteFileTree.main(self.tree)
        #需要重新部署否则不会充满左侧Frame
        self.tree.grid(row=0, column=0, sticky=tk.NSEW)

    def task(self):
        '''这里放置耗时的button程序，用来执行系统命令'''
        self.Resultlist.insert(tk.END, "正在进行弱口令探测...\n")
        if self.cmd == 'scrapy crawl WeakpwdSpider':
            popen = subprocess.Popen('scrapy crawl WeakpwdSpider -a start_url=http://192.168.177.161/dvwa/login.php',
                                     stdout=subprocess.PIPE)
            popen.communicate()
            popen = subprocess.Popen(self.cmd+' -a start_url=' + self.tgtEntry.get(), stdout=subprocess.PIPE)
            # popen1 = subprocess.Popen('scrapy crawl LinkSpider -a start_url=' + self.tgtEntry.get(), stdout=subprocess.PIPE)
            # popen1.communicate()
        else:
            popen = subprocess.Popen('scrapy crawl WeakpwdSpider -a start_url=' + self.tgtEntry.get(),
                                     stdout=subprocess.PIPE)
            # popen1 = subprocess.Popen('scrapy crawl LinkSpider -a start_url=' + self.tgtEntry.get(), stdout=subprocess.PIPE)
            # popen2 = subprocess.Popen(cmd, stdout=subprocess.PIPE)

        self.insertTreeNode()


    def starting(self):
        '''为task方法单独开一个线程'''
        self.thread = threading.Thread(target=self.task())
        self.thread.start()

    def getHistogramResult(self):
        '''获取柱状图扫描结果'''
        vuln = GetVuln.GetVuln()
        allvlunnum = vuln.getAllVuln_num()
        sqlinum = vuln.getSqliVuln_num()
        xssnum = vuln.getXssVuln_num()
        crlfnum = vuln.getCrlfVuln_num()
        weakpwdnum = vuln.getWeakpwdVuln_num()
        print(allvlunnum)
        values = (0,0,crlfnum,allvlunnum-sqlinum-crlfnum,sqlinum)
        print(values)
        return values

    def getPiechartResult(self):
        '''获取饼图扫描结果'''
        vuln = GetVuln.GetVuln()
        allvlunnum = vuln.getAllVuln_num()
        sqlinum = vuln.getSqliVuln_num()
        xssnum = vuln.getXssVuln_num()
        crlfnum = vuln.getCrlfVuln_num()
        weakpwdnum = vuln.getWeakpwdVuln_num()
        values = [xssnum,sqlinum,crlfnum,weakpwdnum]
        print(values)
        return values

    def getResultlist(self):
        '''获取扫描漏洞结果'''
        vuln = GetVuln.GetVuln()
        allvulninfo = vuln.getAllVuln_url()
        allnum = vuln.getAllVuln_num()
        if allnum != 0:
            self.Resultlist.insert(tk.END,'############共探测到'+str(allnum) +'个漏洞############\n')
            for info in allvulninfo:
                self.Resultlist.insert(tk.END,info['vulntype'] + ':\n' + info['vulnurl'] + '\n\n')
        else:
            self.Resultlist.insert(tk.END, '您的网站不存在SQL注入、弱口令、XSS、CRLF漏洞\n')

    def update_result(self):
        '''更新结果'''
        self.insertTreeNode()
        if self.getPiechartResult() != [0,0,0,0]:
            self.Histogram = Histogram.main(self.ScanGraphView,self.getHistogramResult())
            self.PieChart = PieChart.main(self.ScanGraphView,self.getPiechartResult())
        else:
            # 添加柱状图部分初始显示所有的漏洞都是0
            self.Histogram = Histogram.main(self.ScanGraphView,(0,0,0,0,0))
            #添加饼图部分,初始显示每种类型漏洞都为0，所以比例都一样
            self.PieChart = PieChart.main(self.ScanGraphView,[25,25,25,25])
        self.getResultlist()


if (__name__ == '__main__'):
    root = tk.Tk()

    # root.option_add("*Font", "宋体")
    root.minsize(800, 480)
    app = MForm(root)
    root.mainloop()