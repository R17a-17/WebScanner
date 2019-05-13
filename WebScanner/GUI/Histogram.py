#--Created by WD
#python 3.6
#coding:utf-8

import math
import numpy as np
# -------------------------------------------------------------------------------------------
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.pylab import mpl
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk  # NavigationToolbar2TkAgg
# ------------------------------------------------------------------------------------------
import tkinter as tk

# ------------------------------------------------------------------------------------------


mpl.rcParams['font.sans-serif'] = ['SimHei']  # 中文显示
mpl.rcParams['axes.unicode_minus'] = False  # 负号显示


class Histogram:
    def __init__(self, root, data):
        self.root = root  # 创建主窗体
        self.canvas1 = tk.Canvas()  # 创建一块显示图形的画布
        self.data = data
        self.figure = self.create_matplotlib()  # 返回matplotlib所画图形的figure对象
        self.create_form(self.figure)  # 将figure显示在tkinter窗体上面

    def create_matplotlib(self):
        # 创建绘图对象f
        f = plt.figure(num=2, figsize=(7, 2), dpi=80, facecolor="WhiteSmoke", edgecolor='green', frameon=True)
        # 创建一副子图
        # fig1 = plt.subplot(1, 1, 1)

        maxvalue = max(self.data)
        height = max(self.data)
        span = maxvalue/5

        # 设置每根柱子的颜色
        colors = ['forestgreen', 'mediumblue', 'gold', 'r', 'maroon']

        # 绘制柱状图
        plt.bar(np.arange(len(self.data)), self.data, color=colors)

        # 设置柱状图的标题、横坐标标签、纵坐标标签
        plt.title(u'柱状图-等级漏洞个数统计')
        plt.xlabel(u'漏洞类型')
        plt.ylabel(u'个数')

        # 添加横纵坐标的刻度
        labels = [u'信息', u'低危', u'中危', u'高危', u'紧急']
        plt.xticks(range(len(labels)), labels)
        plt.yticks(np.arange(0, int(height), int(span)))

        return f

    def create_form(self, figure):
        # 把绘制的图形显示到tkinter窗口上
        self.canvas1 = FigureCanvasTkAgg(figure, self.root)
        self.canvas1.draw()  # 以前的版本使用show()方法，matplotlib 2.2之后不再推荐show（）用draw代替，但是用show不会报错，会显示警告
        self.canvas1.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # 把matplotlib绘制图形的导航工具栏显示到tkinter窗口上
        # toolbar = NavigationToolbar2Tk(self.canvas1,
        #                                self.root)  # matplotlib 2.2版本之后推荐使用NavigationToolbar2Tk，若使用NavigationToolbar2TkAgg会警告
        # toolbar.update()
        self.canvas1._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

def main(frame, data):
    form = Histogram(frame, data)

if __name__ == "__main__":
    root = tk.Tk()
    frame = tk.Frame(root)
    frame.pack()
    main(frame,(20,40,60,10,4))
    root.mainloop()
