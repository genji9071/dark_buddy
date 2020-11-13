#!/usr/bin/python
# -*- coding: UTF-8 -*-
# 数据库连接配置

# mysql配置
import os

host = os.environ.get("MYSQL_HOST")
port_mysql = int(os.environ.get("MYSQL_PORT"))
user_mysql = os.environ.get("MYSQL_USERNAME")
password_mysql = os.environ.get("MYSQL_PASSWORD")
db_mysql = os.environ.get("MYSQL_DBNAME")

# redis配置
port_redis = int(os.environ.get("REDIS_PORT"))
password_redis = os.environ.get("REDIS_PASSWORD")
