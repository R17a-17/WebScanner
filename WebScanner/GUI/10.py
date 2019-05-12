#--Created by WD
#python 3.6
#coding:utf-8
import tkinter
from tkinter import ttk  # 导入内部包
from WebScanner.GUI.Node import TreeNode
list = [{'file1': 'catalogue', 'file2': 'set-me-free_988', 'file3': 'index.html', 'file4': None, 'file5': None, 'file6': None, 'flag' : '0'},
        {'file1': 'catalogue', 'file2': 'shakespeares-sonnets_989', 'file3': 'index.html', 'file4': None, 'file5': None, 'file6': None, 'flag' : 'file'},
        {'file1': 'catalogue', 'file2': 'starving-hearts-triangular-trade-trilogy-1_990', 'file3': 'index.html', 'file4': None, 'file5': None, 'file6': None}]

win = tkinter.Tk()
tree = ttk.Treeview(win)
myid0 = tree.insert("", 0, "网站目录", text="网站目录", values=("1"))

treenode=TreeNode('网站目录')
for fileset in list:
    id = fileset['file1']
    if treenode.__contains__(id):
        a1=treenode.find_child(treenode,id)
        if a1.__contains__(fileset['file2']):
            a2=a1.find_child(a1,fileset['file3'])
            if a2.__contains__(fileset['file3']):
                a3=a2.find_child(a2,fileset['file4'])
            else:
                a2.add_child(fileset['file4'])
        else:
            a1.add_child(fileset['file3'])
    else:
        a4=treenode.add_child(fileset['file1'])
        a1=a4.add_child(fileset['file2'])
        a2=a1.add_child(fileset['file3'])
        a3 = a2.add_child(fileset['file4'])
treenode.dump()
# i = 0
# for fileset in list:
#     a = tree.get_children('网站目录')
#     id = fileset['file1']
#     print(id)
#     if id != None and id not in a:
#         a1=treenode.add_child(id)
#         # 根节点下添加一级节点,是本层第0个节点，默认状态为关闭，名称为fileset['file1']
#         node1 = tree.insert(myid0, i, '1'+id, open=False, text=id)
#         id1 = '1'+id
#         id =fileset['file2']
#         a = tree.get_children(id1)
#         if id != None and id not in a:
#             a2=treenode.add_child(id)
#             # 第二节点下添加一级节点,是本层第0个节点，默认状态为关闭，名称为fileset['file2']
#             node2 = tree.insert(id1, i, '2'+id, open=False, text=id)
#             id1 = '2'+id
#             id = fileset['file3']
#             a = tree.get_children(id1)
#             if id != None and id not in a:
#                 a3=treenode.add_child(id)
#                 # 第二节点下添加一级节点,是本层第0个节点，默认状态为关闭，名称为fileset['file2']
#                 node2 = tree.insert(id1, i, '3'+id, open=False, text=id)
#                 id1 = '3'+id
#                 id = fileset['file4']
#                 a = tree.get_children(id1)
#                 if id != None and id not in a:
#                     a4=treenode.add_child(id)
#                     # 第二节点下添加一级节点,是本层第0个节点，默认状态为关闭，名称为fileset['file2']
#                     node2 = tree.insert(id1, i, '4' + id, open=False, text=id)
#                 else:
#                     pass
#             else:
#                 pass
#         else:
#             pass
#     else:
#         #保留重复的节点名，以免被覆盖
#         id1 = id
#         #获取下一节点的所有子节点名称
#         a = tree.get_children(id)
#         print(a)
#         id = fileset['file2']
#         #检测file需要存在并且id节点名不重复
#         if id != None and id not in a:
#             #插入子节点
#             node2 = tree.insert(id1, 0, '2'+id, open=False, text=id)
#
#             id1 = id
#             id = fileset['file3']
#             a = tree.get_children(id)
#             if id != None and id not in a:
#                 node3 = tree.insert(id1, 0, '3'+id, open=False, text=id)
#
#                 id1 = id
#                 id = fileset['file4']
#                 a = tree.get_children(id)
#                 if id != None and id not in a:
#                     node4 = tree.insert(id1, 0, '4'+id, open=False, text=id)
#                 else:
#                     pass
#             else:
#                 pass
#         else:
#             pass
#     i = i+1





# 参数:parent, index, iid=None, **kw (父节点，插入的位置，id，显示出的文本)
# myid0 = tree.insert("", 0, "国家", text="国家", values=("1"))
# myid = tree.insert(myid0, 0, "中国", text="中国China", values=("1"))  # ""表示父节点是根
# myidx1 = tree.insert(myid, 0, "广东", text="中国广东", values=("2"))  # text表示显示出的文本，values是隐藏的值
# myidx2 = tree.insert(myid, 1, "江苏", text="中国江苏", values=("3"))
# myidy = tree.insert(myid0, 1, "美国", text="美国USA", values=("4"))
# myidy1 = tree.insert(myidy, 0, "加州", text="美国加州", values=("5"))
# try:
#     i = '中国'
#     myid = tree.insert("", 0, i, text="中国China", values=("1"))
# except tkinter.TclError as e:
#     a = tree.get_children('国家')
#     myidyt = tree.insert('国家', 1, "英国", text="美国USA", values=("4"))
#     print(e)
#     print(a)

tree.pack()
win.mainloop()
