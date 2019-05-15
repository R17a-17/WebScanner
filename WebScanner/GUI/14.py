from socket import *
from tkinter import *
import time
import threading
import re


# GUI窗口类
class Control():
    # 定义GUI界面
    def __init__(self, master, fuc):
        self.parent = master
        self.parent.title("服务器配置器")
        self.frame = Frame(self.parent)
        self.frame.pack(fill=BOTH, expand=3)
        self.parent.resizable(width=False, height=False)

        self.label = Label(self.frame, text="端口设置")

        self.label.grid(row=0, column=0, sticky=E)
        self.entry = Entry(self.frame)
        self.entry.grid(row=0, column=1, sticky=W + E)

        self.label2 = Label(self.frame, text="访问日志")
        self.label2.grid(row=1, column=0, rowspan=6, sticky=W + N)
        self.list = Listbox(self.frame, width=100, height=40)
        self.list.grid(row=3, column=1, rowspan=6, sticky=E + S)

        self.stBtn = Button(self.frame, text="开始服务", command=fuc)
        self.stBtn.grid(row=10, column=1, sticky=W + E)


# 具体功能类
class ThreadClient():
    def __init__(self, master):
        self.master = master
        self.gui = Control(master, self.starting)  # 将我们定义的GUI类赋给服务类的属性，将执行的功能函数作为参数传入
        print(threading.currentThread().ident)

    # 获取请求日志
    def get_log(self, addr, message):
        timenow = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        way = message.decode('utf-8').split()[0]
        resorce = message.decode('utf-8').split()[1][1:]
        info = timenow + ": " + "client:" + str(addr) + " way: " + way + " resorce: " + resorce
        return info

     # 监听方法
    def start_listen(self):
        print(threading.currentThread().ident)
        host = '192.168.177.1'  # 对应本机所有ip地址
        port = int(self.gui.entry.get())  # TCP socket端口
        if not port:
            port = 80
        address = (host, port)
        serverSocket = socket(AF_INET, SOCK_STREAM)  # 创建TCP socket
        serverSocket.bind(address)  # 绑定地址
        serverSocket.listen(1)  # 开始监听
        keepalive = False
        while True:
            try:
                # if not keepalive:
                connectionSocket, clientAddr = serverSocket.accept()  # 获取「连接套接字」
                print("create------")
                print("recv the http request")
                message = connectionSocket.recv(1024)  # 获得http报文
                print("request", message.decode('utf-8'))
                info = self.get_log(clientAddr, message)
                self.gui.list.insert(END, info)
                filename = message.split()[1]  # 获得URI，去掉首部'/'就是文件名
                keepalive = len(re.findall(r'keep-alive', message.decode('utf-8')))
                f = open(filename[1:], 'rb')

                outputdata = f.readlines()  # 逐行读出文件内容并存到list中
                connectionSocket.send('HTTP/1.1 200 OK\r\n\r\n'.encode('utf-8'))  # 发response行

                for i in range(0, len(outputdata)):
                    connectionSocket.send(outputdata[i])  # 把文件各行数据塞到response中 send只能是string类型
                # if not keepalive:
                connectionSocket.close()  # 关闭数据连接

            except IOError:
                connectionSocket.send("404 not found".encode('utf-8'))  # 文件不存在时异常处理
                connectionSocket.close()
        serverSocket.close()

    # 为方法开一个单独的线程
    def starting(self):
        self.thread = threading.Thread(target=self.start_listen)
        self.thread.start()


if __name__ == '__main__':
    root = Tk()
    print(threading.currentThread().ident)
    tool = ThreadClient(root)
    root.mainloop()
