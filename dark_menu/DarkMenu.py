# coding=utf-8
import traceback

from config.ChatbotsConfig import chatbots
from config.TenantConfig import tenant_base_info
from dark_menu.BaseHandler import BaseHandler
from lib.BaseChatbot import CardItem, ActionCard
from lib.Logger import log


class DarkMenu:
    def __init__(self):
        pass

    def get_request_and_send(self, request, json):
        cursor = tenant_base_info[json['chatbotUserId']]['menu']
        paths = []
        if len(request) == 0:
            return self.send_help_action_card(paths, json)
        request_array = request.split(':')
        for request_unit in request_array:
            cursor = cursor.get(request_unit)
            if cursor is None:
                return self.send_help_action_card(paths, json)
            cursor = cursor.get('children')
            if isinstance(cursor, BaseHandler):
                return cursor.do_handle(request_array, json)
            paths.append(request_unit)
        return self.send_help_action_card(paths, json)

    def call_api(self, json):
        request = json["text"]["content"]
        request = request.strip()
        if len(request) == 0:
            request = '**'
        index = request.find("**")
        if index != 0:
            return False
        try:
            request = request[index + len('**'):]
            # 字符预处理
            request = request.replace("：", ":")
            request = request.replace("。", ".")
            request = request.replace("，", ",")
            request = request.replace("！", "!")
            request = request.replace("？", "?")
            self.get_request_and_send(request, json)
            return True
        except:
            log.error(traceback.format_exc())
            return True

    def send_help_action_card(self, paths, request_json):
        cursor = tenant_base_info[request_json['chatbotUserId']]['menu']
        for path in paths:
            cursor = cursor.get(path).get('children')
        btns = []
        for key in cursor.keys():
            if cursor.get(key).get('hidden') == True:
                continue
            btn = CardItem(
                title=key, url=cursor.get(key).get('path'))
            btns.append(btn)
        title = "你是想问？"
        if len(paths) == 0:
            text = "# 你进入了控制台, 你是想问？".format(str(paths))
        else:
            text = "# 关于你的指令：{0}, 你是想问？".format(str(paths))
        action_card = ActionCard(
            title=title, text=text, btns=btns, btn_orientation=1)
        chatbots.get(request_json['chatbotUserId']
                     ).send_action_card(action_card)
        pass


dark_menu = DarkMenu()
