#--Created by WD
#python 3.6
#coding:utf-8
import re
import requests


def form_find(html):
    '''在登录页面的响应中找到form表单，并根据表单属性等获取fromdata'''

    formlist = []
    parameter_list = {}
    formdatalist = []
    # 匹配form表单列表
    if re.finditer(r'<form.*>([\s\S])*</form>', html) == None:
        return None
    for form in re.finditer(r'<form.*>([\s\S])*</form>', html):
        tgtform = form.group()


    if re.finditer(r'<input[^>]+>', str(tgtform)) == None:
        return None
    # 匹配form里面的所有参数和值
    for q in re.finditer(r'<input[^>]+>', str(tgtform)):
        namematch = re.finditer('name="(?P<name>[^ ]+)"', q.group())
        if namematch == None:
            break
        else:
            for match in namematch:
                name = match.group('name')
            valuematch = re.finditer('value="(?P<value>[^ ]+)"', q.group())
            value = ''
            if valuematch != None:
                for match1 in valuematch:
                    value = match1.group('value')
            parameter_list.update({name: value})
            # formdatalist.append(parameter_list)

    return parameter_list

if __name__ == '__main__':
    html = requests.get('http://192.168.177.161/dvwa/login.php').text
    form_find(html)