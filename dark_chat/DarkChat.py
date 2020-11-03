# coding=utf-8
from config.ChatbotsConfig import chatbots
from dark_chat.dark_jikipedia.DarkJikipedia import dark_jikipedia
from dark_chat.dark_qa.DarkQa import dark_qa
from dark_chat.simsimi_chat.SimsimiChat import simsimi_chat


class Dark_chat():

    def __init__(self):
        # 0：暗黑模式
        # 1：普通模式（废弃）
        # 2：智能模式
        # 3：小鸡模式
        self.dark_mode_flag = 3

    def switch_dark_mode(self, request_json):
        request = request_json["text"]["content"]
        if "开启暗黑模式" in request:
            self.dark_mode_flag = 0
            chatbots.get(request_json['chatbotUserId']).send_text("所以我就开启了暗黑模式")
            return True
        if "开启智能模式" in request:
            self.dark_mode_flag = 2
            chatbots.get(request_json['chatbotUserId']).send_text("所以我就开启了智能模式")
            return True
        if "开启小鸡模式" in request:
            self.dark_mode_flag = 3
            chatbots.get(request_json['chatbotUserId']).send_text("所以我就开启了小鸡模式")
            return True
        return False

    def do_dark_chat(self, request_json, dark_mode_flag = -1):
        if self.switch_dark_mode(request_json):
            return
        if dark_mode_flag < 0:
            dark_mode_flag = self.dark_mode_flag
        if dark_mode_flag is 0:
            simsimi_chat.get_simsimi_chat(request_json)
        elif dark_mode_flag is 2:
            dark_qa.get_dark_qa(request_json)
        elif dark_mode_flag is 3:
            dark_jikipedia.get_dark_jikipedia(request_json)

dark_chat = Dark_chat()