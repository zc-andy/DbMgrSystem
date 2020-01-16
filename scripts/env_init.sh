#!/bin/bash

django_path="db_system/django"

yum install -y gcc
yum install -y epel-release
yum install -y python3 python3-wheel python3-devel

pip3 install sqlparser
pip3 install pytz
pip3 install asgiref

cd $django_path && python3 setup.py install
