import requests

key = 'b03c5fa60d08e7d086f553b432ec1141'

true_or_false = 'http://api.tianapi.com/txapi/decide/index?key={0}'
multiple_choice = 'http://api.tianapi.com/txapi/baiketiku/index?key={0}'
just_lick_it = 'http://api.tianapi.com/txapi/tiangou/index?key={0}'

def get_true_or_false():
    return get_data(true_or_false.format(key))

def get_multiple_choice():
    return get_data(multiple_choice.format(key))

def get_just_lick_it():
    return get_data(just_lick_it.format(key))

def get_data(request: str):
    response = requests.get(request)
    if response.status_code != 200:
        raise response.status_code
    return eval(response.content)