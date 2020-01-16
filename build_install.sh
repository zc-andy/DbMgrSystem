# !/bin/bash

cur_path=`pwd` 
pkg_path="db_system_install_$1"
django_path="db_system/django"
config_path="db_system/config"

function init()
{
	echo "INFO[ begin... ]"
	if [ ! -d $pkg_path ] ; then
		mkdir -p $pkg_path
	fi
	
	cd $pkg_path && rm -rf *
	mkdir -p dependence
	mkdir -p db_system

	echo "INFO[ copy django ]"
	cp -r $cur_path/$django_path db_system
	cp -r $cur_path/$config_path db_system

	echo "INFO[ copy scripts ]"
	cp -r $cur_path/scripts/env_init.sh .
	cp -r $cur_path/scripts/setup.sh .
}

function create_django()
{
	cd $cur_path/$pkg_path/dependence
	django-admin startproject django_server
	cp -r $cur_path/db_system/config/django/settings.py django_server/django_server
	cp -r $cur_path/db_system/ui/* django_server
}

# 主程序
function main()
{
	init
	create_django

	cd $cur_path	
	tar -zcvf "$pkg_path".tgz $pkg_path
}
main
