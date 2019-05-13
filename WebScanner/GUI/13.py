#--Created by WD
#python 3.6
#coding:utf-8

import time
import threading
from tkinter import *



def set_ch():
    '''设置中文无法显示的问题'''

    from pylab import mpl
    mpl.rcParams['font.sans-serif'] = ['FangSong']  # 指定默认字体
    mpl.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号显示为方块的问题


def make_plotjpg():
    '''绘制漏洞统计树状图并保存成图片'''

    import matplotlib.pyplot as plt
    import numpy as np

    set_ch()  # 设置中文正常显示
    data = (1,2,4,6,7)
    height = 8
    span = 2
    print(data,height,span)
    print(len(data))

    # 设置每根柱子的颜色
    colors = ['forestgreen', 'mediumblue', 'gold', 'r', 'maroon']

    # 绘制柱状图
    plt.bar(np.arange(len(data)), data, color=colors)

    # 设置柱状图的标题、横坐标标签、纵坐标标签
    plt.title(u'漏洞个数统计')
    plt.xlabel(u'漏洞类型')
    plt.ylabel(u'个数')

    # 添加横纵坐标的刻度
    labels = [u'信息', u'低危', u'中危', u'高危', u'紧急']
    plt.xticks(range(len(labels)), labels)
    plt.yticks(np.arange(0, int(height), int(span)))
    plt.savefig('11.png')

    plt.show()
    plt.close()




def main():
    make_plotjpg()


if __name__ == '__main__':
    main()

