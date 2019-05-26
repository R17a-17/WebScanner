CREATE DATABASE `webscanner` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;


#提取的url存储表
create table t_link_tmp
(
  id   INT(10)     NOT NULL AUTO_INCREMENT,
  link VARCHAR(256) NOT NULL,
  PRIMARY KEY (id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

#保存漏洞详情，包括隐患url、隐患类型
create table t_vuln_url
(
  id INT(10) NOT NULL AUTO_INCREMENT,
  vulnurl VARCHAR(256) NOT NULL,
  vulntype varchar(256) NOT NULL ,
  PRIMARY KEY (id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

#漏洞信息维护表，维护每种漏洞的详细信息包括类型、风险级别、危害和修复建议
create table t_vuln_suggesstion
(
  id INT(10) NOT NULL AUTO_INCREMENT,
  vulntype varchar(256) NOT NULL ,
  vulnlevel int(2) NOT NULL ,
  vulnaffection text NOT NULL ,
  vulnsuggestion text NOT NULL ,
  PRIMARY KEY (id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

#漏洞探测码和响应码维护
create table t_vuln_patterncode
(
  id INT(10) NOT NULL AUTO_INCREMENT,
  vulntype VARCHAR(256) NOT NULL,
  requestcode varchar(256) NOT NULL ,
  responsecode varchar(256) NOT NULL ,
  PRIMARY KEY (id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;