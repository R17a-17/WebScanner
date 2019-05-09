from tkinter import *
import tkinter.messagebox as messagebox


def createpage(master):
    master = Frame(root)
    master.pack()
    Label(master, text='num1').grid(row=0, column=0, stick=W, pady=10)
    e1 = Entry(master)
    e1.grid(row=0, column=1, stick=E)
    Label(master, text='num2').grid(row=1, column=0, stick=W, pady=10)
    e2 = Entry(master)
    e2.grid(row=1, column=1, stick=E)
    # Button传递参数
    Button(
        master, text='加', command=lambda: btn_def(e1.get(), e2.get())
    ).grid(row=2, column=0, stick=W)
    Button(master, text='减').grid(row=2, column=1, stick=E)
    Label(master, text='说明').grid(row=3, column=0, stick=W, pady=10)
    Label(master, text='只写了加法(请输入简单数字测试button传参)').grid(
        row=3, column=1, stick=E
    )


def btn_def(num1, num2):
    num = int(num1) + int(num2)
    messagebox.showinfo('结果', '%d' % num)


if __name__ == '__main__':
    root = Tk()
    root.title('Demo')
    root.geometry('400x150')
    createpage(root)
    root.mainloop()