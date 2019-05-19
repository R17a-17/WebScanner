#--Created by WD
#python 3.6
#coding:utf-8

# import tkinter
#
#
# tkinter.filedialog.asksaveasfilename()   # 选择以什么文件名保存，返回文件名
# tkinter.filedialog.askopenfilename()     # 选择打开什么文件，返回文件名
#
#
# # root = tkinter.Tk()    # 创建一个Tkinter.Tk()实例
# # root.withdraw()       # 将Tkinter.Tk()实例隐藏
# # default_dir = r"文件路径"
# # file_path = tkinter.filedialog.askopenfilename(title=u'选择文件', initialdir=(os.path.expanduser(default_dir)))
# # image = Image.open(file_path)
# # plt.imshow(image)
# # plt.show()
#
# fname = tkinter.filedialog.asksaveasfilename(title=u'保存文件', filetypes=[("PNG", ".png")])
# # picture.save(str(fname) + '.png', 'PNG')
#
# root = tkinter.Tk()    # 创建一个Tkinter.Tk()实例
# root.withdraw()       # 将Tkinter.Tk()实例隐藏

from tkinter.filedialog import asksaveasfilename
from WebScanner.Report import piechart_pic
import tkinter
from WebScanner.Report import word
# root = tkinter.Tk()    # 创建一个Tkinter.Tk()实例
# root.withdraw()       # 将Tkinter.Tk()实例隐藏
# # fname = askopenfilename(filetypes=(("Template files", "*.tplate"), ("HTML files", "*.html;*.htm"),("All files", "*.*")))
# fname = tkinter.filedialog.asksaveasfilename(title=u'保存文件', filetypes=[("PNG", ".png")])
# picture = piechart_pic.make_piechartpng((1,5,3,1))
#
# picture.savefig(str(fname) + '.png')
root = tkinter.Tk()  # 创建一个Tkinter.Tk()实例
root.withdraw()  # 将Tkinter.Tk()实例隐藏
fname = asksaveasfilename(title=u'保存文件', filetypes=[("DOCX",".docx")])
# picture = piechart_pic.make_piechartpng((1, 5, 3, 1))
wordfile = word.main('1213', scantime='5分钟', scanurlnum=51)
wordfile.save(str(fname) + '.docx')