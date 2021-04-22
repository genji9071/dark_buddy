import re

import requests


# 83051
def get_random_number(number):
    f = requests.get(f'http://www.pythonchallenge.com/pc/def/linkedlist.php?busynothing={number}')
    print(f.text)
    reg = re.compile('and the next busynothing is (\\d+)')
    result = ''.join(reg.findall(f.text))
    if len(result) == 0:
        return 1
    else:
        return result


if __name__ == '__main__':
    number = 83051
    while number != 1:
        number = get_random_number(number)
