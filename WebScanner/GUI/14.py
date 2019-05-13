#--Created by WD
#python 3.6
#coding:utf-8

#本脚本用于显示各类型漏洞的占比情况

import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
font = FontProperties('FangSong', size=14)


nums = [1,50,29,20]

label = ['XSS','SQLI','CRLF','Weak Password']
color = ['red','green','yellow','purple']

indic = []

#我们将数据最大的突出显示
for value in nums:
    if value == max(nums):
        indic.append(0.1)
    else:
        indic.append(0)

plt.pie(
    nums,
    labels=label,
    colors=color,
    startangle=90,
    shadow=True,
    explode=tuple(indic),#tuple方法用于将列表转化为元组
    autopct='%1.1f%%'#是数字1，不是l
)


plt.title(u'饼图—统计各类型漏洞所占比例', FontProperties=font)

plt.show()
