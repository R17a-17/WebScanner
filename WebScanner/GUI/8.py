from tkinter import *
import datetime
import threading


def do_word():      # 这里没特别的需求不需要动
    global a
    if a:
        t = threading.Thread(target=task)
        t.setDaemon(True)
        t.start()
    root.after(100,do_word)

def task():
    # 这里放超耗时间的东西，如请求服务器，读或写文件等。
    # 注意的是一般读写分离，
    # 读文件一条线程，写文件一条线程或者使用队列就不用分两条线程操作了。
    dd = datetime.datetime.now()
    label['text'] = dd


def one_word():
    print('开始')
    global a
    a = 1

def quit_word():
    print('暂停')
    global a
    a =0

# 说是多线程这里只用了一个线程，仅供参考。
# 作者：hhaoao

##########################gui############################
a = 0       # 控制线程的开关
root = Tk()
button = Button(root,text='开始',command=one_word)
quit_button = Button(root,text='暂停',command=quit_word)
label = Label(root,text='redy...')

button.grid()
quit_button.grid()
label.grid()
do_word()
root.mainloop()
