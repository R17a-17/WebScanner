#--Created by WD
#python 3.6
#coding:utf-8

# 本脚本用于制作漏洞统计柱状图


def set_ch():
    '''设置中文无法显示的问题'''

    from pylab import mpl
    mpl.rcParams['font.sans-serif'] = ['FangSong']  # 指定默认字体
    mpl.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号显示为方块的问题


def make_histogrampng(data):
    '''绘制漏洞统计树状图并保存成图片'''

    import matplotlib.pyplot as plt
    import numpy as np

    set_ch()  # 设置中文正常显示

    maxvalue = max(data)
    height = max(data)
    span = 0
    if maxvalue == 0:
        span = 0
    else:
        span = maxvalue / 5
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
    try:
        plt.yticks(np.arange(0, int(height), int(span)))
    except ZeroDivisionError as e:
        plt.yticks(np.arange(0, 0, 1))
    fname = '../reporttmp/pic1.png'
    plt.savefig(fname)

    plt.close()
    return fname


def main():
    make_histogrampng((0,5,3,8,1))


if __name__ == '__main__':
    main()

