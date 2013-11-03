
-- database
create database if if not exists cbrc_dev_blog default character set utf8;

-- table

-- project 项目
create table if not exists project (
	id int not null,
	name varchar(256) not null,
	abbr_name varchar(256),
	description varchar(256),
	owner_id int,
	create_time timestamp,
	last_update_time timestamp
) engine InnoDB comment '项目';

-- article 文章
create table if not exists article (
	id bigint not null,
	project_id int,
	author_id int,
	title varchar(256) not null,
	content text,
	create_time timestamp,
	publish_time timestamp,
	last_update_time timestamp
) engine innodb comment '文章';

-- user 用户
create table if not exists user (
	id int not null,
	login_name varchar(32) not null unique,
	email varchar(64),
	name varchar(64),
	address varchar(128),
	description varchar(512),
	create_time timestamp,
	last_update_time timestamp
) engine innodb comment '用户';

-- tag 标签
create table if not exists tag (
	id bigint not null,
	name varchar(32) not null,
	author_id int,
	create_time timestamp,
	last_update_time timestamp
) engine innodb comment '标签';

-- article_tag
create table if not exists article_tag (
	article_id bigint not null,
	tag_id int not null
) engine innodb comment '文章的标签';


insert into user (id, login_name, email, name, address, description, create_time, last_update_time) 
	values (1, 'hwangsyin', 'hwangsyin@gmail.com', '信息中心开发团队博客项目发起人', '中国北京', '鉴于信息中心软件开发及发布流程现状开发了该博客系统', 
	'2013-11-02 09:00:00.000', '2013-11-02 09:00:00.000');

insert into project (id, name, abbr_name, description, owner_id, create_time, last_update_time) 
	values(1, '信息中心开发团队博客', '信息中心开发团队博客', '源代码仓库: https://github.com/hwangsyin/cbrc-devteam-blog', 
	1, '2013-11-02 09:00:00.000', '2013-11-02 09:00:00.000');
	
insert into article (id, project_id, author_id, title, content, create_time, publish_time, last_update_time)
	values(1, 1, 1, '关于信息中心开发团队博客', '为什么有这个博客项目', '2013-11-02 09:00:00.000',
	'2013-11-02 09:00:00.000', '2013-11-02 09:00:00.000');
