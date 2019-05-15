#--Created by WD
#python 3.6
#coding:utf-

#————————————————————————
#外部包导入
import tkinter as tk
from tkinter import messagebox
import threading
import os
import subprocess
#-----------------------------------------------
#内部包导入
from WebScanner.GUI import Verify
from WebScanner.GUI.GuiApplication import MForm
#--------------------------------------------------


CMD = {
    'XSS':'scrapy crawl XssSpider',
    'SQL注入':'scrapy crawl SqliSpider',
    'CRLF': 'scrapy crawl CRLF',
    '弱口令': 'scrapy crawl WeakpwdSpider',
    '综合扫描':'scrapy crawl VulndetectSpider',
}


class ThreadClient():
    def __init__(self, master):
        self.master = master
        self.gui = MForm(master, self.starting)  # 将我们定义的GUI类赋给服务类的属性，将执行的功能函数作为参数传入
        print(threading.currentThread().ident)


    def task(self):
        '''这里放置耗时的button程序，用来执行系统命令'''
        print(threading.currentThread().ident)
        self.gui.scanButton.config(state=tk.DISABLED)
        if Verify.Verify_tgt(self.gui.tgtEntry.get()):
            messagebox.showwarning(title='警告', message='输入的目标url无效！请重新输入')
            self.gui.scanButton.config(state=tk.NORMAL)
            return
        elif Verify.Verify_combox(self.gui.comboxlist.get()):
            messagebox.showwarning(title='警告', message='请选择配置')
            self.gui.scanButton.config(state=tk.NORMAL)
            return
        else:
            self.gui.Resultlist.insert(tk.END, "开启WebScanner...\n")
            self.gui.cmd = CMD[self.gui.comboxlist.get()]
            self.gui.cmdvalue.set(self.gui.cmd + ' -a start_url=' + self.gui.tgtEntry.get())
            print(self.gui.cmd)
            self.gui.Resultlist.insert(tk.END, "正在进行弱口令探测...\n")
            if self.gui.cmd == 'scrapy crawl WeakpwdSpider':
                popen = subprocess.Popen('scrapy crawl WeakpwdSpider -a start_url=http://192.168.177.161/dvwa/login.php',
                    stdout=subprocess.PIPE)
                while True:
                    if popen.stdout.readline() == b'':
                        break
                    self.gui.Resultlist.insert(tk.END,popen.stdout.readline().decode('utf8'))
                popen.communicate()
                os.system('scrapy crawl LinkSpider -a start_url=http://192.168.177.161/dvwa/login.php')
            elif self.gui.cmd == 'scrapy crawl VulndetectSpider':
                os.system('scrapy crawl WeakpwdSpider -a start_url=http://192.168.177.161/dvwa/login.php')
                os.system('scrapy crawl LinkSpider -a start_url=http://192.168.177.161/dvwa/login.php')
            else:
                os.system('scrapy crawl WeakpwdSpider -a start_url=http://192.168.177.161/dvwa/login.php')
                os.system('scrapy crawl LinkSpider -a start_url=http://192.168.177.161/dvwa/login.php')
                os.system(self.gui.cmd)
        self.gui.scanButton.config(state=tk.NORMAL)
        self.gui.GetResultButton.config(state = tk.NORMAL)
        self.gui.Resultlist.insert(tk.END,'探测完成！请点击获取结果。\n')
        # self.gui.update_result()



    # 为方法开一个单独的线程
    def starting(self):
        self.thread = threading.Thread(target=self.task)
        self.thread.start()




#################################################################################################

if (__name__ == '__main__'):
    root = tk.Tk()
    root.minsize(800, 480)
    print(threading.currentThread().ident)
    tool = ThreadClient(root)
    root.mainloop()