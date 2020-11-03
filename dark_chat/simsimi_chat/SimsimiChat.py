#coding=utf-8
import traceback

import requests

from config.ChatbotsConfig import chatbots
from config.SimsimiConfig import simsimi_url, get_simsimi_body, simsimi_header
from lib.Logger import log


class Simsimi_chat():

    def __init__(self):
        self.url = simsimi_url

    def get_simsimi_chat(self, request_json):
        request = request_json["text"]["content"]
        body = get_simsimi_body(request)
        header = simsimi_header
        response = requests.post(self.url, json=body, headers=header)
        text = response.text.replace("true", "True").replace("false", "False").replace("null", "None")
        response_json = eval(text)
        if response_json["status"] != 200:
            log.error(traceback.format_exc())
            log.error(response.text)
            chatbots.get(request_json['chatbotUserId']).send_text("你这是说的什么弟弟鬼话呢！")
            return False
        datas = response_json["atext"]
        chatbots.get(request_json['chatbotUserId']).send_text(datas)
        return True

simsimi_chat = Simsimi_chat()
