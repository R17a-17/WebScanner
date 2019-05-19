CREATE DATABASE `webscanner` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;


create table t_link_tmp
(
  id   INT(10)     NOT NULL AUTO_INCREMENT,
  link VARCHAR(256) NOT NULL,
  PRIMARY KEY (id)
);

select * from t_link_tmp;

insert into t_link_tmp(link) values ('http://192.168.177.161/dvwa/vulnerabilities/xss_r/?name=#');
insert into t_link_tmp(link) values ('http://192.168.177.161/dvwa/vulnerabilities/sqli_blind/?id=1&Submit=%C8%B7%B6%A8#');

delete from t_link_tmp;

#删除临时链接表，重新从1开始计id
truncate table t_link_tmp;

#去重
DELETE
FROM
    shop
WHERE
    shopid NOT IN ( SELECT temp.id FROM ( SELECT min( shopid ) AS id FROM shop GROUP BY shopurl ) AS temp );





create table t_vulninfo
(
  id INT(10) NOT NULL AUTO_INCREMENT,
  vulnurl VARCHAR(256) NOT NULL,
  vulntype varchar(256) NOT NULL ,
  vulnlevel varchar(256) NOT NULL ,
  vulnaffection text NOT NULL ,
  vulnsuggestion text NOT NULL ,
  PRIMARY KEY (id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

drop table t_vulninfo;

select * from t_vulninfo;


insert into t_vulninfo(vulnurl, vulntype, vulnlevel, vulnaffection, vulnsuggestion) values ('http://adfsdsf','XSS','高危','1）网络钓鱼，盗取各类用户的账号 。
    2）窃取用户Cookie，获取用户隐私或管理员权限，利用用户身份进一步执行操作，例如进行非法转账、强制发表日志等 。
    3）强制弹出广告页面，刷流量等。
    4）进行恶意操作，例如任意篡改页面信息，删除文章等，传播跨站脚本蠕虫，网页挂马等 。
    5）进行基于大量的客户端攻击，如DDOS攻击。','每个提交信息的客户端页面，通过服务器端脚本（JSP、ASP、ASPX、PHP等脚本）生成的客户端页面，提交的表单（FORM）或发出的连接请求中包含的所有变量，必须对变量的值进行检查。过滤其中包含的特殊字符，或对字符进行转义处理。特殊字符包括：
HTML标签的<符号、“符号、’符号、%符号等，以及这些符号的Unicode值；
客户端脚本（Javascript、VBScript）关键字：javascript、script等；
此外，对于信息搜索功能，不应在搜索结果页面中回显搜索内容。同时应设置出错页面，防止Web服务器发生内部错误时，错误信息返回给客户端。');

truncate table t_vulninfo;

select sleep(if(1=1),5,0);

select * from t_link_tmp where id=1 and 2=sleep(5);


truncate table t_link_tmp;
truncate table t_vulninfo;