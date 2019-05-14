

#--Created by WD
#python 3.6
#coding:utf-8

from scrapy import *
from pymysql import *
import re
import random
from scrapy.conf import settings
from WebScanner.items_xss import XssItem


#XSS:javascript开始符号
XSS_START = [
    "<script>", "<Script>"
]

#XSS:javascript结束符号
XSS_END = [
    "</script>","</Script>"
]

#javascript的一些弹窗标签
XSS_JS_WINDOW = [
    "alert", "confirm", "prompt"
]

#xss:JavaScript on*事件触发函数
XSS_JS_ONARRAY = [
    'onload' , 'onerror' , 'onmousemove', 'onclick', 'onsubmit', 'onmouseover', 'onfocus',
    'onloadeddata', 'onwaiting', 'onredo', 'onprogress', 'ondragenter', 'onreset', 'onended',
    'onmousedown', 'onforminput', 'onhaschange', 'ondurationchange', 'onpause', 'onplay',
    'onmousewheel', 'onchange', 'onafterprint', 'oninvalid', 'onloadstart', 'onabort',
    'oninput', 'onmouseout', 'ondragover', 'onsuspend', 'ontimeupdate', 'onratechange',
    'ondragleave', 'onresize', 'onselect', 'onundo', 'onemptied', 'ondrag', 'oncanplay',
    'onstorage', 'onformchange', 'onblur', 'ondragstart', 'onoffline', 'ondrop', 'onkeypress',
    'ononline', 'onkeydown', 'onpageshow', 'onvolumechange', 'onpopstate', 'oncontextmenu',
    'onscroll','onunload', 'onloadedmetadata', 'ondragend', 'onseeking', 'onbeforeprint',
    'oncanplaythrough', 'onbeforeunload', 'onpagehide', 'onmouseup', 'onkeyup', 'onmessage',
    'onplaying', 'ondblclick', 'onseeked', 'onreadystatechange', 'onstalled'
]

#html标签类的xss,
HTMLTAG_XSS_START = [
    "<video src", "<audio src", "<img src", "<a href", "<iframe src"
]

HTMLTAG_XSS_END = [
    "</video>", "</audio>", "</img>" ,"</a>", "</iframe>"
]


class XssSpider(Spider):
    '''针对每个页面做出探测特征码请求，然后根据响应包进行响应包特征码的探测'''

    name = "XssSpider"


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
        self.url = self.xss_detect()
        self.start_urls.append(self.url)
        #设置cookie便于访问登录后的页面
        self.cookie = settings['COOKIES']

        yield Request(self.start_urls[0], callback=self.parse, cookies=self.cookie)



    def parse(self, response):
        '''处理请求数据并继续下条url'''
        #是否存在可测试的参数
        if self.detect_code:
            if self.xss_response_check(response.body):
                self.linkth = self.linkth + 1
                xssitem = XssItem()
                xssitem['vulnurl'] = self.url
                yield xssitem
                if self.level == 1:
                    print(r'存在xss漏洞:JavaScript窗口注入')
                elif self.level == 2:
                    print(r'存在xss漏洞：HTML标签注入')
                elif self.level == 3:
                    print(r'存在xss漏洞：JavaScript触发事件响应函数')
            elif self.level < 3:
                self.level = self.level + 1
            else:
                self.level = 1
                print(r'不存在xss漏洞')
                self.linkth = self.linkth + 1
        else:
            print(r'不存在xss漏洞')
            self.linkth = self.linkth + 1

        self.url = self.geturlfrommysql(self.linkth)

        if self.url:
            self.url = self.xss_detect()
            print("正在测试第%d个url"%self.linkth)
            # 如果找到下一页的URL，构造新的Request 对象
            yield Request(self.url, callback=self.parse, cookies = self.cookie)




    def xss_detect(self):
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
            parameter_num = random.randint(0, len(list)-1)
            parameter = list[parameter_num]['parameter']
            value = list[parameter_num]['value']
            #替换前字符串
            oldstr = parameter + '=' + value
            print("Scanning %s for xss in parameter '%s'" % (url, parameter))
            #根据level等级生成探测码
            self.detect_code = eval('self.generate_detectcode_level' + str(self.level))()
            value = value + self.detect_code
            #参数和探测值生成新的字符串
            newstr = parameter + '=' + value
            #将url替换成探测url
            url = url.replace(oldstr, newstr)
        else:
            self.detect_code = None

        return url


    def xss_response_check(self, body):
        '''检测响应包中是否还有特征码'''
        body = str(body).lower()
        if body.find(self.detect_code.lower()) >= 0:
            return True
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


    def generate_detectcode_level1(self):
        '''生成探测码，险level级为1，探测码为普通JavaScript窗口：XSS_JS_WINDOW'''
        # 在XSS_START列表中随机取一个
        i = random.randint(0, len(XSS_START) - 1)
        # 在XSS_JS_WINDOW列表随机取一个
        j = random.randint(0, len(XSS_JS_WINDOW) - 1)
        detect_code = XSS_START[i] + XSS_JS_WINDOW[0] + '(' + str(random.randint(1, 9999)) + ')' + XSS_END[i]
        return detect_code


    def generate_detectcode_level2(self):
        '''生成探测码，level级别为2，当level1检测失败，启用level2，探测码为HTML危险标签：HTMLTAG_XSS'''
        # 在HTMLTAG_XSS列表中随机取一个
        i = random.randint(0, len(HTMLTAG_XSS_START) - 1)
        detect_code = HTMLTAG_XSS_START[i] + '=' + str(random.randint(1, 99)) + '.html>XSS test' + HTMLTAG_XSS_END[i]
        return detect_code


    def generate_detectcode_level3(self):
        '''生成探测码，level级别为3，当level2检测失败，启用level3，探测码为JavaScript事件触发函数：XSS_JS_ONARRAY'''
        # 在XSS_START列表中随机取一个
        i = random.randint(0, len(XSS_START) - 1)
        # 在XSS_JS_ONARRAY列表随机取一个
        j = random.randint(0, len(XSS_JS_ONARRAY) - 1)
        #在XSS_JS_WINDOW列表中随机取一个
        k = random.randint(0,len(XSS_JS_WINDOW)-1)
        detect_code = XSS_START[i] + XSS_JS_ONARRAY[j] + '=' + XSS_JS_WINDOW[k] + '(' + str(random.randint(1, 9999)) + ')' + XSS_END[i]
        return detect_code