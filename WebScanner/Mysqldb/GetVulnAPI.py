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
        '''获取xss信息'''
        sql = 'select vulntype,vulnurl from t_vuln_url where vulntype like "XSS%"'
        # sql = 'INSERT INTO t_link_tmp(link) SELECT %s FROM DUAL WHERE NOT EXISTS(SELECT link from t_link_tmp where link = %s)'
        self.db_cur.execute(sql)
        try:
            for vuln in self.db_cur.fetchone():
                xsstype = vuln[0]
                xssurl = vuln[1]
                xssinfo = [xsstype, xssurl]
        except:
            xssinfo = None
        return xssinfo

    def getSqliVuln_url(self):
        '''获取sqli信息'''
        sql = 'select vulntype,vulnurl from t_vuln_url where vulntype linke "SQLI%"'
        # sql = 'INSERT INTO t_link_tmp(link) SELECT %s FROM DUAL WHERE NOT EXISTS(SELECT link from t_link_tmp where link = %s)'
        self.db_cur.execute(sql)
        try:
            for vuln in self.db_cur.fetchone():
                sqlitype = vuln[0]
                sqliurl = vuln[1]
                sqliinfo = [sqlitype, sqliurl]
        except:
            sqliinfo = None
        return sqliinfo

    def getCrlfVuln_url(self):
        '''获取sqli信息'''
        sql = 'select vulntype,vulnurl from t_vuln_url where vulntype linke "CRLF%"'
        # sql = 'INSERT INTO t_link_tmp(link) SELECT %s FROM DUAL WHERE NOT EXISTS(SELECT link from t_link_tmp where link = %s)'
        self.db_cur.execute(sql)
        try:
            for vuln in self.db_cur.fetchone():
                crlftype = vuln[0]
                crlfurl = vuln[1]
                crlfinfo = [crlftype, crlfurl]
        except:
            crlfinfo = None
        return crlfinfo

    def getWeakpwdVuln_url(self):
        '''获取sqli信息'''
        sql = 'select vulntype,vulnurl from t_vuln_url where vulntype linke "Weak Password%"'
        # sql = 'INSERT INTO t_link_tmp(link) SELECT %s FROM DUAL WHERE NOT EXISTS(SELECT link from t_link_tmp where link = %s)'
        self.db_cur.execute(sql)
        try:
            for vuln in self.db_cur.fetchone():
                weakpwdtype = vuln[0]
                weakpwdurl = vuln[1]
                weakpwdinfo = [weakpwdtype, weakpwdurl]
        except:
            weakpwdinfo = None
        return weakpwdinfo

    def getAllVuln_url(self):
        '''获取sqli信息'''
        allinfo = []
        sql = 'select vulntype,vulnurl from t_vuln_url'
        # sql = 'INSERT INTO t_link_tmp(link) SELECT %s FROM DUAL WHERE NOT EXISTS(SELECT link from t_link_tmp where link = %s)'
        self.db_cur.execute(sql)
        try:
            result = self.db_cur.fetchall()
            for vuln in result:
                alltype = vuln[0]
                allurl = vuln[1]
                try:
                    type = alltype.split(':')[0]
                except:
                    type = alltype
                vulninfo = self.getVuln_suggestion(type)
                alllevel = vulninfo[0]['vulnlevel']
                allaffection = vulninfo[0]['vulnaffection']
                allsuggestion = vulninfo[0]['vulnsuggestion']
                allinfo.append({'vulntype':alltype, 'vulnurl':allurl, 'vulnlevel':alllevel, 'vulnaffection':allaffection,'vulnsuggestion':allsuggestion})
        except:
            allinfo = None
        return allinfo

    def getXssVuln_num(self):
        '''获取xss信息'''
        sql = 'select count(*) from t_vuln_url where vulntype like "XSS%"'
        # sql = 'INSERT INTO t_link_tmp(link) SELECT %s FROM DUAL WHERE NOT EXISTS(SELECT link from t_link_tmp where link = %s)'
        self.db_cur.execute(sql)
        try:
            xssnum = self.db_cur.fetchone()[0]
        except:
            xssnum = 0
        return xssnum

    def getSqliVuln_num(self):
        '''获取sqli漏洞数量'''
        sql = 'select count(*) from t_vuln_url where vulntype like "SQLI%"'
        # sql = 'INSERT INTO t_link_tmp(link) SELECT %s FROM DUAL WHERE NOT EXISTS(SELECT link from t_link_tmp where link = %s)'
        self.db_cur.execute(sql)
        try:
            sqlinum = self.db_cur.fetchone()[0]
        except:
            sqlinum = 0
        return sqlinum

    def getCrlfVuln_num(self):
        '''获取sqli漏洞数量'''
        sql = 'select count(*) from t_vuln_url where vulntype like "CRLF%"'
        # sql = 'INSERT INTO t_link_tmp(link) SELECT %s FROM DUAL WHERE NOT EXISTS(SELECT link from t_link_tmp where link = %s)'
        self.db_cur.execute(sql)
        try:
            crlfnum = self.db_cur.fetchone()[0]
        except:
            crlfnum = 0
        return crlfnum

    def getWeakpwdVuln_num(self):
        '''获取sqli漏洞数量'''
        sql = 'select count(*) from t_vuln_url where vulntype like "Weak Password%"'
        # sql = 'INSERT INTO t_link_tmp(link) SELECT %s FROM DUAL WHERE NOT EXISTS(SELECT link from t_link_tmp where link = %s)'
        self.db_cur.execute(sql)
        try:
            weakpwdnum = self.db_cur.fetchone()[0]
        except:
            weakpwdnum = 0
        return weakpwdnum

    def getAllVuln_num(self):
        '''获取XSS漏洞数量'''
        sql = 'select count(*) from t_vuln_url'
        # sql = 'INSERT INTO t_link_tmp(link) SELECT %s FROM DUAL WHERE NOT EXISTS(SELECT link from t_link_tmp where link = %s)'
        self.db_cur.execute(sql)
        try:
            allnum = self.db_cur.fetchone()[0]
        except:
            allnum = 0
        return allnum

    def getVuln_suggestion(self,type):
        '''获取漏洞危害和修复建议'''
        likestr = type + '%'
        sql = 'select * from t_vuln_suggesstion where vulntype like %s'
        self.db_cur.execute(sql,likestr)
        vulninfo = []
        vulnfet = self.db_cur.fetchall()
        for vuln in vulnfet:
            vulnlevel = vuln[2]
            vulnaffection = vuln[3]
            vulnsuggestion = vuln[4]
            vulninfo.append(
                { 'vulnlevel':vulnlevel, 'vulnaffection': vulnaffection,'vulnsuggestion': vulnsuggestion}
            )
        return vulninfo

if __name__ == '__main__':
    sql = GetVuln()
    sql.getAllVuln_url()