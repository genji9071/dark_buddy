# coding=utf-8
import bs4
import requests


def calc_expr(expr_text):
    expr_text = expr_text.replace('x', '*')
    return eval(expr_text)


def get_flag():
    url = "http://ctf5.shiyanbar.com/jia/index.php"
    param = "?action=check_pass"
    response = requests.get(url)
    soup = bs4.BeautifulSoup(response.text, "html.parser")
    expr_text = soup.select("form")[0].find("div").text
    ans = calc_expr(expr_text)
    body = {
        "pass_key": ans
    }
    response = requests.post(url+param, body)
    print(response.text)


get_flag()