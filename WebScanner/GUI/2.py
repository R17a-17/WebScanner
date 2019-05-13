from tkinter import *

class ScrollText:
    def __init__(self):

        # 窗口和标题
        window = Tk()
        window.title("滚动条示例")

        # 创建一个纵向滚动的滚动条,打包到窗口右侧，铺满Y方向
        scrollbar = Scrollbar(window,orient=VERTICAL)#orient默认为纵向
        scrollbar.pack(fill=Y, side=RIGHT)

        # 打包一个文本域到窗口，y方向滚动文本的监听丢给滚动条的set函数（文本域主动关联滚动条）
        text = Text(window,width=100, yscrollcommand=scrollbar.set)
        text.pack()

        # 拉动滚动条时，改变文本域在y方向上的视图（滚动条主动关联文本域）
        scrollbar.config(command=text.yview)

        # 消息循环
        window.mainloop()
ScrollText()