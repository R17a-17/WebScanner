#--Created by WD
#python 3.6
#coding:utf-8

import os
import subprocess


def WeakpwdSpider_exec(url, option):
    # 命令行执行WeakpwdSpider，供GUI、CMD调用

    if option == 'Weakpwd':
        cmd = 'scrapy crawl WeakpwdSpider'
    elif option == 'XSS':
        cmd = 'scrapy crawl XssSpider'
    elif option == 'SQLI':
        cmd = 'scrapy crawl SqliSpider'
    elif option == 'CRLF':
        cmd = 'scrapy crawl CRLF'
    elif option == 'Vulndetect':
        cmd = 'scrapy crawl VulndetectSpider'

    print(cmd)
    popen = subprocess.Popen(cmd, stdout=subprocess.PIPE)


# def WeakpwdSpider_exec(url):
#     #命令行执行WeakpwdSpider，供GUI、CMD调用
#     print(url)
#     popen = subprocess.Popen(['scrapy', 'crawl', 'WeakpwdSpider'], stdout = subprocess.PIPE)
#     while True:
#         if popen.stdout.readline() == b'':
#             break
#         v = popen.stdout.readline()
#         print(v)


    # def WeakpwdSpider_exec(self, url):
    #     '''命令行执行WeakpwdSpider，供GUI、CMD调用'''
    #     self.scanButton.config(state=tk.DISABLED)
    #     print(url)
    #     cmd = "scrapy crawl WeakpwdSpider"
    #     print(cmd)
    #     info = os.system(cmd)  # 执行LinkSpider爬取链接
    #     self.info = info.split('\n')
    #     i = len(self.info)
    #     def counter(i):
    #
    #         if i > 1:
    #             self.ScanText.insert(tk.END, self.info[i-1])
    #             self.ScanText.after(1000, counter, i - 1)
    #         else:
    #             self.scanButton.config(state=tk.NORMAL)
    #
    #     self.scanButton.config(state=tk.DISABLED)
    #     counter(i)



if __name__ == "__main__":
    info = WeakpwdSpider_exec(' = StringVar() ')
    print(info)