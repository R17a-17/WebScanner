#--Created by WD
#python 3.6
#coding:utf-8
from pymysql import *

class GetVuln(object):
    '''获取mysql的漏洞信息'''

    def __init__(self):
        self.db_conn = connect(host='localhost', port=3306, db='webscanner', user='root', passwd='toor', charset='utf8')
        self.db_cur = self.db_conn.cursor()

    def getXssVuln_url(self):
        '''获取XSs'''
        sql = 'select vulntype from t_vulninfo where vulntype = "XSS"'
        # sql = 'INSERT INTO t_link_tmp(link) SELECT %s FROM DUAL WHERE NOT EXISTS(SELECT link from t_link_tmp where link = %s)'
        self.db_cur.execute(sql, sql)
        self.db_conn.commit()
        self.db_conn.close()

    def getSqliVuln_url(self):
        '''获取XSs'''
        sql = 'select vulntype from t_vulninfo where vulntype = "SQLI"'
        # sql = 'INSERT INTO t_link_tmp(link) SELECT %s FROM DUAL WHERE NOT EXISTS(SELECT link from t_link_tmp where link = %s)'
        self.db_cur.execute(sql, sql)
        self.db_conn.commit()
        self.db_conn.close()

    def getXssVuln_num(self):
        '''获取XSs'''
        sql = 'select count(*) from t_vulninfo where vulntype = "XSS"'
        # sql = 'INSERT INTO t_link_tmp(link) SELECT %s FROM DUAL WHERE NOT EXISTS(SELECT link from t_link_tmp where link = %s)'
        self.db_cur.execute(sql, sql)
        self.db_conn.commit()
        self.db_conn.close()

    def getSqliVuln_num(self):
        '''获取XSs'''
        sql = 'select count(*) from t_vulninfo where vulntype = "SQLI"'
        # sql = 'INSERT INTO t_link_tmp(link) SELECT %s FROM DUAL WHERE NOT EXISTS(SELECT link from t_link_tmp where link = %s)'
        self.db_cur.execute(sql, sql)
        self.db_conn.commit()
        self.db_conn.close()

    def getAllVuln_num(self):
        '''获取XSs'''
        sql = 'select count(*) from t_vulninfo'
        # sql = 'INSERT INTO t_link_tmp(link) SELECT %s FROM DUAL WHERE NOT EXISTS(SELECT link from t_link_tmp where link = %s)'
        self.db_cur.execute(sql, sql)
        self.db_conn.commit()
        self.db_conn.close()