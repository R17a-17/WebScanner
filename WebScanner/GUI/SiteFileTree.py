# --Created by WD
# python 3.6
# coding:utf-8
import tkinter
from tkinter import ttk  # 导入内部包
from WebScanner.GUI.Node import TreeNode
import re
from pymysql import *


list = []
domain = ''

def sitefile_tree(list,url):
    #生成网站目标的文件树
    #匹配目标网站的目录树的正则表达式
    p = '^(http://)?([\w-]+\.)+[\w-]+(/(?P<file1>[a-zA-Z0-9.?=_#&-]*))?(/(?P<file2>[a-zA-Z0-9.?=_#&-]*))?(/(?P<file3>[a-zA-Z0-9.?=_#&-]*))?(/(?P<file4>[a-zA-Z0-9.?=_#&-]*))?(/(?P<file5>[a-zA-Z0-9.?=_#&-]*))?(/(?P<file6>[a-zA-Z0-9.?=_#&-]*))?(/(?P<file7>[a-zA-Z0-9.?=_#&-]*))?(/(?P<file8>[a-zA-Z0-9.?=_#&-]*))?'
    filetree = re.match(p,url)
    list.append({'file1': filetree.group('file1'),'file2': filetree.group('file2'),'file3': filetree.group('file3'),'file4': filetree.group('file4'),'file5': filetree.group('file5'),'file6': filetree.group('file6'),'file7': filetree.group('file7'),'file8': filetree.group('file8')})
    print(list)


def select_db(db_cur, linkth):
    '''查询链接'''
    sql = 'select link from t_link_tmp where id=%s'
    db_cur.execute(sql, linkth)
    try:
        nextlink = db_cur.fetchone()[0]
    except:
        nextlink = None

    return nextlink


def generate_guitree(tree,myid0, list,domain):

    treenode = TreeNode(domain)
    for fileset in list:
        id = fileset['file1']
        if treenode.__contains__(id) and id != None:
            a1 = treenode.find_child(id)
            node1 = myid0
            if a1.__contains__(fileset['file2']) and fileset['file2'] != None:
                a2 = a1.find_child(fileset['file2'])
                if a2.__contains__(fileset['file3']) and fileset['file3'] != None:
                    a3 = a2.find_child(fileset['file3'])
                    if a3.__contains__(fileset['file4']) and fileset['file4'] != None:
                        a4 = a3.find_child(fileset['file4'])
                        if a4.__contains__(fileset['file5']) and fileset['file5'] != None:
                            a5 = a4.find_child(fileset['file5'])
                            if a5.__contains__(fileset['file6']) and fileset['file6'] != None:
                                a6 = a5.find_child(fileset['file6'])
                                if a6.__contains__(fileset['file7']) and fileset['file7'] != None:
                                    a7 = a6.find_child(fileset['file7'])
                                    if a7.__contains__(fileset['file8']) and fileset['file8'] != None:
                                        pass
                                    elif fileset['file8'] != None:
                                        node8 = tree.insert(
                                            fileset['file1'] + ' ' + fileset['file2'] + ' ' + fileset['file3'] + ' ' +
                                            fileset['file4'] + ' ' + fileset['file5'] + ' ' + fileset['file6'] + ' ' +
                                            fileset['file7'], len(a7) - 1,
                                            fileset['file1'] + ' ' + fileset['file2'] + ' ' + fileset['file3'] + ' ' +
                                            fileset['file4'] + ' ' + fileset['file5'] + ' ' + fileset['file6'] + ' ' +
                                            fileset['file7'] + ' ' + fileset['file8'], open=False,
                                            text=fileset['file8'])
                                        a8 = a7.add_child(fileset['file8'])
                                elif fileset['file7'] != None:
                                    node7 = tree.insert(
                                        fileset['file1'] + ' ' + fileset['file2'] + ' ' + fileset['file3'] + ' ' +
                                        fileset[
                                            'file4'] + ' ' + fileset['file5'] + ' ' + fileset['file6'], len(a6) - 1,
                                        fileset['file1'] + ' ' + fileset['file2'] + ' ' + fileset['file3'] + ' ' +
                                        fileset[
                                            'file4'] + ' ' + fileset['file5'] + ' ' + fileset['file6'] + ' ' + fileset[
                                            'file7'], open=False, text=fileset['file7'])
                                    a7 = a6.add_child(fileset['file7'])
                                    if fileset['file8'] != None:
                                        node8 = tree.insert(
                                            fileset['file1'] + ' ' + fileset['file2'] + ' ' + fileset['file3'] + ' ' +
                                            fileset['file4'] + ' ' + fileset['file5'] + ' ' + fileset['file6'] + ' ' +
                                            fileset['file7'], len(a7) - 1,
                                            fileset['file1'] + ' ' + fileset['file2'] + ' ' + fileset['file3'] + ' ' +
                                            fileset['file4'] + ' ' + fileset['file5'] + ' ' + fileset['file6'] + ' ' +
                                            fileset['file7'] + ' ' + fileset['file8'], open=False,
                                            text=fileset['file8'])
                                        a8 = a7.add_child(fileset['file8'])
                            elif fileset['file6'] != None:
                                node6 = tree.insert(
                                    fileset['file1'] + ' ' + fileset['file2'] + ' ' + fileset['file3'] + ' ' + fileset[
                                        'file4'] + ' ' + fileset['file5'], len(a5) - 1,
                                    fileset['file1'] + ' ' + fileset['file2'] + ' ' + fileset['file3'] + ' ' + fileset[
                                        'file4'] + ' ' + fileset['file5'] + ' ' + fileset['file6'], open=False,
                                    text=fileset['file6'])
                                a6 = a5.add_child(fileset['file6'])
                                if fileset['file7'] != None:
                                    node7 = tree.insert(
                                        fileset['file1'] + ' ' + fileset['file2'] + ' ' + fileset['file3'] + ' ' +
                                        fileset[
                                            'file4'] + ' ' + fileset['file5'] + ' ' + fileset['file6'], len(a6) - 1,
                                        fileset['file1'] + ' ' + fileset['file2'] + ' ' + fileset['file3'] + ' ' +
                                        fileset[
                                            'file4'] + ' ' + fileset['file5'] + ' ' + fileset['file6'] + ' ' + fileset[
                                            'file7'], open=False, text=fileset['file7'])
                                    a7 = a6.add_child(fileset['file7'])
                                    if fileset['file8'] != None:
                                        node8 = tree.insert(
                                            fileset['file1'] + ' ' + fileset['file2'] + ' ' + fileset['file3'] + ' ' +
                                            fileset['file4'] + ' ' + fileset['file5'] + ' ' + fileset['file6'] + ' ' +
                                            fileset['file7'], len(a7) - 1,
                                            fileset['file1'] + ' ' + fileset['file2'] + ' ' + fileset['file3'] + ' ' +
                                            fileset['file4'] + ' ' + fileset['file5'] + ' ' + fileset['file6'] + ' ' +
                                            fileset['file7'] + ' ' + fileset['file8'], open=False,
                                            text=fileset['file8'])
                                        a8 = a7.add_child(fileset['file8'])
                        elif fileset['file5'] != None:
                            node5 = tree.insert(
                                fileset['file1'] + ' ' + fileset['file2'] + ' ' + fileset['file3'] + ' ' + fileset[
                                    'file4'],
                                len(a4) - 1,
                                fileset['file1'] + ' ' + fileset['file2'] + ' ' + fileset['file3'] + ' ' + fileset[
                                    'file4'] + ' ' + fileset['file5'], open=False, text=fileset['file5'])
                            a5 = a4.add_child(fileset['file5'])
                            if fileset['file6'] != None:
                                node6 = tree.insert(
                                    fileset['file1'] + ' ' + fileset['file2'] + ' ' + fileset['file3'] + ' ' + fileset[
                                        'file4'] + ' ' + fileset['file5'], len(a5) - 1,
                                    fileset['file1'] + ' ' + fileset['file2'] + ' ' + fileset['file3'] + ' ' + fileset[
                                        'file4'] + ' ' + fileset['file5'] + ' ' + fileset['file6'], open=False,
                                    text=fileset['file6'])
                                a6 = a5.add_child(fileset['file6'])
                                if fileset['file7'] != None:
                                    node7 = tree.insert(
                                        fileset['file1'] + ' ' + fileset['file2'] + ' ' + fileset['file3'] + ' ' +
                                        fileset[
                                            'file4'] + ' ' + fileset['file5'] + ' ' + fileset['file6'], len(a6) - 1,
                                        fileset['file1'] + ' ' + fileset['file2'] + ' ' + fileset['file3'] + ' ' +
                                        fileset[
                                            'file4'] + ' ' + fileset['file5'] + ' ' + fileset['file6'] + ' ' + fileset[
                                            'file7'], open=False, text=fileset['file7'])
                                    a7 = a6.add_child(fileset['file7'])
                                    if fileset['file8'] != None:
                                        node8 = tree.insert(
                                            fileset['file1'] + ' ' + fileset['file2'] + ' ' + fileset['file3'] + ' ' +
                                            fileset['file4'] + ' ' + fileset['file5'] + ' ' + fileset['file6'] + ' ' +
                                            fileset['file7'], len(a7) - 1,
                                            fileset['file1'] + ' ' + fileset['file2'] + ' ' + fileset['file3'] + ' ' +
                                            fileset['file4'] + ' ' + fileset['file5'] + ' ' + fileset['file6'] + ' ' +
                                            fileset['file7'] + ' ' + fileset['file8'], open=False,
                                            text=fileset['file8'])
                                        a8 = a7.add_child(fileset['file8'])
                    elif fileset['file4'] != None:
                        node4 = tree.insert(fileset['file1'] + ' ' + fileset['file2'] + ' ' + fileset['file3'],
                                            len(a3) - 1,
                                            fileset['file1'] + ' ' + fileset['file2'] + ' ' + fileset['file3'] + ' ' +
                                            fileset['file4'], open=False, text=fileset['file4'])
                        a4 = a3.add_child(fileset['file4'])
                        if fileset['file5'] != None:
                            node5 = tree.insert(
                                fileset['file1'] + ' ' + fileset['file2'] + ' ' + fileset['file3'] + ' ' + fileset[
                                    'file4'],
                                len(a4) - 1,
                                fileset['file1'] + ' ' + fileset['file2'] + ' ' + fileset['file3'] + ' ' + fileset[
                                    'file4'] + ' ' + fileset['file5'], open=False, text=fileset['file5'])
                            a5 = a4.add_child(fileset['file5'])
                            if fileset['file6'] != None:
                                node6 = tree.insert(
                                    fileset['file1'] + ' ' + fileset['file2'] + ' ' + fileset['file3'] + ' ' + fileset[
                                        'file4'] + ' ' + fileset['file5'], len(a5) - 1,
                                    fileset['file1'] + ' ' + fileset['file2'] + ' ' + fileset['file3'] + ' ' + fileset[
                                        'file4'] + ' ' + fileset['file5'] + ' ' + fileset['file6'], open=False,
                                    text=fileset['file6'])
                                a6 = a5.add_child(fileset['file6'])
                                if fileset['file7'] != None:
                                    node7 = tree.insert(
                                        fileset['file1'] + ' ' + fileset['file2'] + ' ' + fileset['file3'] + ' ' +
                                        fileset[
                                            'file4'] + ' ' + fileset['file5'] + ' ' + fileset['file6'], len(a6) - 1,
                                        fileset['file1'] + ' ' + fileset['file2'] + ' ' + fileset['file3'] + ' ' +
                                        fileset[
                                            'file4'] + ' ' + fileset['file5'] + ' ' + fileset['file6'] + ' ' + fileset[
                                            'file7'], open=False, text=fileset['file7'])
                                    a7 = a6.add_child(fileset['file7'])
                                    if fileset['file8'] != None:
                                        node8 = tree.insert(
                                            fileset['file1'] + ' ' + fileset['file2'] + ' ' + fileset['file3'] + ' ' +
                                            fileset['file4'] + ' ' + fileset['file5'] + ' ' + fileset['file6'] + ' ' +
                                            fileset['file7'], len(a7) - 1,
                                            fileset['file1'] + ' ' + fileset['file2'] + ' ' + fileset['file3'] + ' ' +
                                            fileset['file4'] + ' ' + fileset['file5'] + ' ' + fileset['file6'] + ' ' +
                                            fileset['file7'] + ' ' + fileset['file8'], open=False,
                                            text=fileset['file8'])
                                        a8 = a7.add_child(fileset['file8'])
                elif fileset['file3'] != None:
                    node3 = tree.insert(fileset['file1'] + ' ' + fileset['file2'], len(a2) - 1,
                                        fileset['file1'] + ' ' + fileset['file2'] + ' ' + fileset['file3'], open=False,
                                        text=fileset['file3'])
                    a3 = a2.add_child(fileset['file3'])
                    if fileset['file4'] != None:
                        node4 = tree.insert(fileset['file1'] + ' ' + fileset['file2'] + ' ' + fileset['file3'],
                                            len(a3) - 1,
                                            fileset['file1'] + ' ' + fileset['file2'] + ' ' + fileset['file3'] + ' ' +
                                            fileset['file4'], open=False, text=fileset['file4'])
                        a4 = a3.add_child(fileset['file4'])
                        if fileset['file5'] != None:
                            node5 = tree.insert(
                                fileset['file1'] + ' ' + fileset['file2'] + ' ' + fileset['file3'] + ' ' + fileset[
                                    'file4'],
                                len(a4) - 1,
                                fileset['file1'] + ' ' + fileset['file2'] + ' ' + fileset['file3'] + ' ' + fileset[
                                    'file4'] + ' ' + fileset['file5'], open=False, text=fileset['file5'])
                            a5 = a4.add_child(fileset['file5'])
                            if fileset['file6'] != None:
                                node6 = tree.insert(
                                    fileset['file1'] + ' ' + fileset['file2'] + ' ' + fileset['file3'] + ' ' + fileset[
                                        'file4'] + ' ' + fileset['file5'], len(a5) - 1,
                                    fileset['file1'] + ' ' + fileset['file2'] + ' ' + fileset['file3'] + ' ' + fileset[
                                        'file4'] + ' ' + fileset['file5'] + ' ' + fileset['file6'], open=False,
                                    text=fileset['file6'])
                                a6 = a5.add_child(fileset['file6'])
                                if fileset['file7'] != None:
                                    node7 = tree.insert(
                                        fileset['file1'] + ' ' + fileset['file2'] + ' ' + fileset['file3'] + ' ' +
                                        fileset[
                                            'file4'] + ' ' + fileset['file5'] + ' ' + fileset['file6'], len(a6) - 1,
                                        fileset['file1'] + ' ' + fileset['file2'] + ' ' + fileset['file3'] + ' ' +
                                        fileset[
                                            'file4'] + ' ' + fileset['file5'] + ' ' + fileset['file6'] + ' ' + fileset[
                                            'file7'], open=False, text=fileset['file7'])
                                    a7 = a6.add_child(fileset['file7'])
                                    if fileset['file8'] != None:
                                        node8 = tree.insert(
                                            fileset['file1'] + ' ' + fileset['file2'] + ' ' + fileset['file3'] + ' ' +
                                            fileset['file4'] + ' ' + fileset['file5'] + ' ' + fileset['file6'] + ' ' +
                                            fileset['file7'], len(a7) - 1,
                                            fileset['file1'] + ' ' + fileset['file2'] + ' ' + fileset['file3'] + ' ' +
                                            fileset['file4'] + ' ' + fileset['file5'] + ' ' + fileset['file6'] + ' ' +
                                            fileset['file7'] + ' ' + fileset['file8'], open=False,
                                            text=fileset['file8'])
                                        a8 = a7.add_child(fileset['file8'])
            elif fileset['file2'] != None:
                node2 = tree.insert(fileset['file1'], len(a1) - 1, fileset['file1'] + ' ' + fileset['file2'],
                                    open=False,
                                    text=fileset['file2'])
                a2 = a1.add_child(fileset['file2'])
                if fileset['file3'] != None:
                    node3 = tree.insert(fileset['file1'] + ' ' + fileset['file2'], len(a2) - 1,
                                        fileset['file1'] + ' ' + fileset['file2'] + ' ' + fileset['file3'], open=False,
                                        text=fileset['file3'])
                    a3 = a2.add_child(fileset['file3'])
                    if fileset['file4'] != None:
                        node4 = tree.insert(fileset['file1'] + ' ' + fileset['file2'] + ' ' + fileset['file3'],
                                            len(a3) - 1,
                                            fileset['file1'] + ' ' + fileset['file2'] + ' ' + fileset['file3'] + ' ' +
                                            fileset['file4'], open=False, text=fileset['file4'])
                        a4 = a3.add_child(fileset['file4'])
                        if fileset['file5'] != None:
                            node5 = tree.insert(
                                fileset['file1'] + ' ' + fileset['file2'] + ' ' + fileset['file3'] + ' ' + fileset[
                                    'file4'],
                                len(a4) - 1,
                                fileset['file1'] + ' ' + fileset['file2'] + ' ' + fileset['file3'] + ' ' + fileset[
                                    'file4'] + ' ' + fileset['file5'], open=False, text=fileset['file5'])
                            a5 = a4.add_child(fileset['file5'])
                            if fileset['file6'] != None:
                                node6 = tree.insert(
                                    fileset['file1'] + ' ' + fileset['file2'] + ' ' + fileset['file3'] + ' ' + fileset[
                                        'file4'] + ' ' + fileset['file5'], len(a5) - 1,
                                    fileset['file1'] + ' ' + fileset['file2'] + ' ' + fileset['file3'] + ' ' + fileset[
                                        'file4'] + ' ' + fileset['file5'] + ' ' + fileset['file6'], open=False,
                                    text=fileset['file6'])
                                a6 = a5.add_child(fileset['file6'])
                                if fileset['file7'] != None:
                                    node7 = tree.insert(
                                        fileset['file1'] + ' ' + fileset['file2'] + ' ' + fileset['file3'] + ' ' +
                                        fileset[
                                            'file4'] + ' ' + fileset['file5'] + ' ' + fileset['file6'], len(a6) - 1,
                                        fileset['file1'] + ' ' + fileset['file2'] + ' ' + fileset['file3'] + ' ' +
                                        fileset[
                                            'file4'] + ' ' + fileset['file5'] + ' ' + fileset['file6'] + ' ' + fileset[
                                            'file7'], open=False, text=fileset['file7'])
                                    a7 = a6.add_child(fileset['file7'])
                                    if fileset['file8'] != None:
                                        node8 = tree.insert(
                                            fileset['file1'] + ' ' + fileset['file2'] + ' ' + fileset['file3'] + ' ' +
                                            fileset['file4'] + ' ' + fileset['file5'] + ' ' + fileset['file6'] + ' ' +
                                            fileset['file7'], len(a7) - 1,
                                            fileset['file1'] + ' ' + fileset['file2'] + ' ' + fileset['file3'] + ' ' +
                                            fileset['file4'] + ' ' + fileset['file5'] + ' ' + fileset['file6'] + ' ' +
                                            fileset['file7'] + ' ' + fileset['file8'], open=False,
                                            text=fileset['file8'])
                                        a8 = a7.add_child(fileset['file8'])
        elif id != None:
            node1 = tree.insert(myid0, 0, fileset['file1'], open=False, text=fileset['file1'])
            a1 = treenode.add_child(fileset['file1'])
            if fileset['file2'] != None:

                node2 = tree.insert(fileset['file1'], len(a1) - 1, fileset['file1'] + ' ' + fileset['file2'],
                                    open=False,
                                    text=fileset['file2'])
                a2 = a1.add_child(fileset['file2'])
                if fileset['file3'] != None:
                    node3 = tree.insert(fileset['file1'] + ' ' + fileset['file2'], len(a2) - 1,
                                        fileset['file1'] + ' ' + fileset['file2'] + ' ' + fileset['file3'], open=False,
                                        text=fileset['file3'])
                    a3 = a2.add_child(fileset['file3'])
                    if fileset['file4'] != None:
                        node4 = tree.insert(fileset['file1'] + ' ' + fileset['file2'] + ' ' + fileset['file3'],
                                            len(a3) - 1,
                                            fileset['file1'] + ' ' + fileset['file2'] + ' ' + fileset['file3'] + ' ' +
                                            fileset['file4'], open=False, text=fileset['file4'])
                        a4 = a3.add_child(fileset['file4'])
                        if fileset['file5'] != None:
                            node5 = tree.insert(
                                fileset['file1'] + ' ' + fileset['file2'] + ' ' + fileset['file3'] + ' ' + fileset[
                                    'file4'],
                                len(a4) - 1,
                                fileset['file1'] + ' ' + fileset['file2'] + ' ' + fileset['file3'] + ' ' + fileset[
                                    'file4'] + ' ' + fileset['file5'], open=False, text=fileset['file5'])
                            a5 = a4.add_child(fileset['file5'])
                            if fileset['file6'] != None:
                                node6 = tree.insert(
                                    fileset['file1'] + ' ' + fileset['file2'] + ' ' + fileset['file3'] + ' ' + fileset[
                                        'file4'] + ' ' + fileset['file5'], len(a5) - 1,
                                    fileset['file1'] + ' ' + fileset['file2'] + ' ' + fileset['file3'] + ' ' + fileset[
                                        'file4'] + ' ' + fileset['file5'] + ' ' + fileset['file6'], open=False,
                                    text=fileset['file6'])
                                a6 = a5.add_child(fileset['file6'])
                                if fileset['file7'] != None:
                                    node7 = tree.insert(
                                        fileset['file1'] + ' ' + fileset['file2'] + ' ' + fileset['file3'] + ' ' +
                                        fileset[
                                            'file4'] + ' ' + fileset['file5'] + ' ' + fileset['file6'], len(a6) - 1,
                                        fileset['file1'] + ' ' + fileset['file2'] + ' ' + fileset['file3'] + ' ' +
                                        fileset[
                                            'file4'] + ' ' + fileset['file5'] + ' ' + fileset['file6'] + ' ' + fileset[
                                            'file7'], open=False, text=fileset['file7'])
                                    a7 = a6.add_child(fileset['file7'])
                                    if fileset['file8'] != None:
                                        node8 = tree.insert(
                                            fileset['file1'] + ' ' + fileset['file2'] + ' ' + fileset['file3'] + ' ' +
                                            fileset['file4'] + ' ' + fileset['file5'] + ' ' + fileset['file6'] + ' ' +
                                            fileset['file7'], len(a7) - 1,
                                            fileset['file1'] + ' ' + fileset['file2'] + ' ' + fileset['file3'] + ' ' +
                                            fileset['file4'] + ' ' + fileset['file5'] + ' ' + fileset['file6'] + ' ' +
                                            fileset['file7'] + ' ' + fileset['file8'], open=False,
                                            text=fileset['file8'])
                                        a8 = a7.add_child(fileset['file8'])
    treenode.dump()

def main(tree):
    db_conn = connect(host='localhost', port=3306, db='webscanner', user='root', passwd='toor', charset='utf8')
    db_cur = db_conn.cursor()
    linkth = 1
    url = select_db(db_cur, linkth)
    p = '^(http://)?(?P<domain>([\w-]+\.)+[\w-]+)(/(?P<file1>[a-zA-Z0-9.?=_#&-]*))?(/(?P<file2>[a-zA-Z0-9.?=_#&-]*))?(/(?P<file3>[a-zA-Z0-9.?=_#&-]*))?(/(?P<file4>[a-zA-Z0-9.?=_#&-]*))?(/(?P<file5>[a-zA-Z0-9.?=_#&-]*))?(/(?P<file6>[a-zA-Z0-9.?=_#&-]*))?(/(?P<file7>[a-zA-Z0-9.?=_#&-]*))?(/(?P<file8>[a-zA-Z0-9.?=_#&-]*))?'
    domain = re.match(p,url).group('domain')
    print(domain)
    while url != None:
        sitefile_tree(list, url)
        linkth = linkth+1
        url = select_db(db_cur, linkth)
        print(url)
    myid0 = tree.insert("", 0, domain, text=domain, values=("1"))
    generate_guitree(tree,myid0,list,domain)
    tree.pack()



if __name__ == '__main__':


    win = tkinter.Tk()
    tree = ttk.Treeview(win)
    main(tree)
    win.mainloop()
