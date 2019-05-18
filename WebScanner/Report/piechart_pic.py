#--Created by WD
#python 3.6
#coding:utf-8



def set_ch():
    '''设置中文无法显示的问题'''

    from pylab import mpl
    mpl.rcParams['font.sans-serif'] = ['FangSong']  # 指定默认字体
    mpl.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号显示为方块的问题


def make_piechartpng(data):
    '''绘制漏洞统计树状图并保存成图片'''

    import matplotlib.pyplot as plt
    import numpy as np
    set_ch()  # 设置中文正常显示

    nums = [1, 50, 29, 20]

    label = ['XSS', 'SQLI', 'CRLF', 'WeakPwd']
    color = ['red', 'green', 'yellow', 'purple']

    indic = []

    # 我们将数据最大的突出显示
    for value in data:
        if value == max(data):
            indic.append(0.1)
        else:
            indic.append(0)

    plt.pie(
        data,
        labels=label,
        colors=color,
        startangle=90,
        shadow=True,
        explode=tuple(indic),  # tuple方法用于将列表转化为元组
        autopct='%1.1f%%'  # 是数字1，不是l
    )

    plt.title(u'饼图—统计各类型漏洞所占比例')

    fname = 'pic2.png'
    plt.savefig(fname)

    plt.close()
    return fname


def main():
    make_histogrampng((0,5,3,1))


if __name__ == '__main__':
    main()




