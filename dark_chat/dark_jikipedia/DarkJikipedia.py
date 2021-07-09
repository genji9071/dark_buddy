# coding=utf-8
from urllib.parse import quote

import requests

from config.ChatbotsConfig import chatbots
from config.JikipediaConfig import auto_complete_url, search_definitions_url, browse_definitions_url, header
from dark_menu.BaseHandler import BaseHandler
from lib.BaseChatbot import ActionCard, CardItem


class DarkJikipedia(BaseHandler):

    def __init__(self):
        self.auto_complete_url = auto_complete_url
        self.search_definitions_url = search_definitions_url
        self.browse_definitions_url = browse_definitions_url
        self.header = header

    def get_dark_jikipedia(self, request_json):
        text = request_json["text"]["content"].strip()

        # 1：补全搜索条件
        if self.auto_complete(text, request_json):
            return True

        # 2：搜TMD
        search_definition_data = self.search_definitions(text)

        # 3: 发TMD
        if search_definition_data == {}:
            chatbots.get(request_json['chatbotUserId']).send_text("小鸡我搜不到东西了，你换个方式再问一遍")
        else:
            action_card = self.action_card_content(search_definition_data)
            chatbots.get(request_json['chatbotUserId']).send_action_card(action_card)
        return True

    def auto_complete(self, text, request_json):
        body = {
            "phrase": text
        }
        response = requests.post(self.auto_complete_url, json=body, headers=self.header)
        # log.info(json.dumps(response.json(), indent=4))
        auto_complete_result = response.json()['data']
        if len(auto_complete_result) > 0:
            btns = []
            for word in auto_complete_result:
                if text == word['word']:
                    return False
                title = word['word']
                btn = CardItem(title=title,url="dtmd://dingtalkclient/sendMessage?content={0}".format(quote(title)))
                btns.append(btn)
            title = "你是想问？"
            text = "### 你是想问？"
            action_card = ActionCard(title=title, text=text, btns=btns)
            chatbots.get(request_json['chatbotUserId']).send_action_card(action_card)
            return True
        return False

    def search_definitions(self, text):
        body = {
            "page": 1,
            "phrase": text
        }
        response = requests.post(self.search_definitions_url, json=body, headers=self.header).json()
        # log.info(json.dumps(response, indent=4))
        datas = response['data']
        # check 同名结果
        max_like = 0
        max_like_data = {}
        max_the_same_like = 0
        max_the_same_like_data = {}
        for data in datas:
            score = data['like_count']
            if len(data.get('images')) > 0:
                score = score * 1.5
            if data['term']['title'] == text:
                if score > max_the_same_like:
                    max_the_same_like = data['like_count']
                    max_the_same_like_data = data
            else:
                if score > max_like:
                    max_like = data['like_count']
                    max_like_data = data
        if max_the_same_like > 0:
            return max_the_same_like_data
        else:
            return max_like_data

    def action_card_content(self, search_definition_data):
        title = search_definition_data['term']['title']
        content = search_definition_data['plaintext']
        image_url = search_definition_data.get('images')
        if len(image_url) == 0:
            text = '### {0}\n{1}\n'.format(title, content)
        else:
            text = '![screenshot]({0})\n### {1}\n{2}\n'.format(image_url[0]['scaled']['path'], title, content.strip())
        return ActionCard(title=title, text=text,
                          btns=[CardItem(title="查看更多", url="dtmd://dingtalkclient/sendMessage?content=**骚词:推荐")])

    def do_handle(self, request_object, request_json):
        body = {}
        response = requests.post(self.browse_definitions_url, json=body, headers=self.header).json()
        # log.info(json.dumps(response, indent=4))
        content = "### 骚词推荐\n"
        for data in response:
            if data.get('scaled_image') != '':
                title = data.get('term').get('title')
                content += "[{0}](dtmd://dingtalkclient/sendMessage?content={1})/".format(title, quote(title))
        action_card = ActionCard(
            title="骚词推荐",
            text=content[:-1],
            btns=[CardItem(title="查看更多", url="dtmd://dingtalkclient/sendMessage?content=**骚词:推荐")]
        )
        chatbots.get(request_json['chatbotUserId']).send_action_card(action_card)
        return True


dark_jikipedia = DarkJikipedia()
