CREATE DATABASE `webscanner` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;


create table t_link_tmp
(
  id   INT(10)     NOT NULL AUTO_INCREMENT,
  link VARCHAR(256) NOT NULL,
  PRIMARY KEY (id)
);

select * from t_link_tmp;

delete from t_link_tmp;


truncate table t_link_tmp;


create table t_vulninfo
(
  id INT(10) NOT NULL AUTO_INCREMENT,
  vulnurl VARCHAR(256) NOT NULL,
  vulntype varchar(256) NOT NULL ,
  origin_request TEXT NOT NULL ,
  origin_response TEXT NOT NULL ,
  detect_request TEXT NOT NULL ,
  detect_response TEXT not null ,
  PRIMARY KEY (id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

select * from t_vulninfo;
