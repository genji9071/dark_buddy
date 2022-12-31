import os

import requests

from config.ChatbotsConfig import chatbots
from dark_menu.BaseHandler import BaseHandler
from lib.BaseChatbot import ActionCard, CardItem


class ZuAnChat(BaseHandler):

    zuan_url = 'https://nmsl.shadiao.app/api.php?lang=zh_cn'
    mini_url = 'https://nmsl.shadiao.app/api.php?level=min&lang=zh_cn'
    flag = True
    zuan_response_list = ''

    def __init__(self):
        zuan_response = open(os.path.split(os.path.realpath(__file__))[0] + '/resources/zuan_response.txt', 'r', encoding='utf-8')
        self.zuan_response_list = zuan_response.readlines()

    def do_handle(self, request_object, request_json):
        action_card = ActionCard(title='祖安',
                                 text='# ' + self.getZuAn(), btns=[
                CardItem(title="你再骂？！", url="**祖安")])
        chatbots.get(request_json['chatbotUserId']).send_action_card(action_card)

    def getZuAn(self):
        # if self.flag:
        url = self.mini_url
        # else:
        #     url = self.zuan_url
        response = requests.get(url)
        self.flag = not self.flag
        return str(response.text)

zuan_chat = ZuAnChat()