#!/bin/bash

cur_path=`pwd`
system_path="/db_system"

# 数据库初始化
function mysql_init()
{
	yum -y install mariadb
	yum -y install mariadb-server
	yum -y install mariadb-devel
	pip3 install mysqlclient

	cd $cur_path
	systemctl start mariadb
	mysqladmin -u root password "my_db"
	mysql -u root -pmy_db < db_system/config/sql/sql_init.sql
}

#初始化
function init()
{
	# 环境部署
	sh env_init.sh

	mysql_init

	# 开放80端口
	firewall-cmd --zone=public --add-port=80/tcp --permanent
	firewall-cmd --reload
}

#构建系统目录
function create_system()
{
	if [ ! -d $system_path ] ; then
		mkdir -p $system_path
	fi

	rm -rf $system_path/*
	cp -r dependence/* $system_path

	cd $system_path/django_server && python3 manage.py migrate
}

#主程序
function main()
{
	init

	create_system
}
main
