import pickle

import requests

if __name__ == '__main__':
    banner = requests.get('http://www.pythonchallenge.com/pc/def/banner.p')
    p = pickle.loads(banner.content)
    for line in p:
        output = ''
        for per in line:
            output += per[0] * per[1]
        print(output)
