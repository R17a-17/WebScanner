#--Created by WD
#python 3.6
#coding:utf-8
import re

def Verify_tgt(tgt):
    # 验证目标url是否输入正确
    url_pattern = '^(http://)?([\w-]+\.)+[\w-]+([A-Za-z0-9/-?%&=\._]*)?$'
    v = re.match(url_pattern, tgt)
    if v == None:
        return True
    return False

if __name__ == '__main__':
    a = Verify_tgt('1')
    print(a)