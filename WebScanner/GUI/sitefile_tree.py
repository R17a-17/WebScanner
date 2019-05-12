#--Created by WD
#python 3.6
#coding:utf-8


import re
from pymysql import *

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


def main():
    list = []
    db_conn = connect(host='localhost', port=3306, db='webscanner', user='root', passwd='toor', charset='utf8')
    db_cur = db_conn.cursor()
    linkth = 1
    url = select_db(db_cur, linkth)
    while url != None:
        sitefile_tree(list, url)
        linkth = linkth+1
        url = select_db(db_cur, linkth)

    print(list)
    return list


