# coding=utf-8
import time
import uuid
from urllib.parse import quote

import requests

import config
import dark_word_cloud.CloudMaker as cloudMaker
from config import redis
from config.ChatbotsConfig import chatbots
from dark_chat.dark_jikipedia.DarkJikipedia import dark_jikipedia
from dark_menu.BaseHandler import BaseHandler
from lib.BaseChatbot import ActionCard
from lib.ImageFactory import image_factory


class DarkJiWordCloud(BaseHandler):
    def do_handle(self, request_object, request_json):
        id = uuid.uuid1()
        image = self.get_image()
        words = self.get_words()
        if image == '':
            chatbots.get(request_json['chatbotUserId']
                         ).send_text('正在生成中，这可能需要一些时间...')
            body = {}
            word_cloud_dict = {}
            while len(word_cloud_dict) < 200:
                response = requests.post(
                    dark_jikipedia.browse_definitions_url, json=body, headers=dark_jikipedia.header).json()
                for data in response:
                    word_cloud_dict[data.get('term').get(
                        'title')] = data.get('view_count')
                    if len(word_cloud_dict) == 200:
                        break
                time.sleep(1)
            image = cloudMaker.make_word_cloud_to_image(word_cloud_dict)
            self.put_image(image)
            id = uuid.uuid1()
            words = self.put_words(word_cloud_dict)
        title = "小鸡骚词"
        img_url = f"http://{config.public_ip}/dark_buddy/dark_ji_word_cloud/image/get?session_id={request_json['chatbotUserId']}&uuid={id}"
        text = f"![screenshot]({img_url})\n### 小鸡骚词\n{words}"
        action_card = ActionCard(title=title, text=text, btns=[], img_url=img_url)
        chatbots.get(request_json['chatbotUserId']
                     ).send_action_card(action_card)

    def put_image(self, image):
        data = image_factory.image_to_base64(image)
        redis.setex(name=self.get_redis_key(), time=3600 * 12,
                    value=data)
        return

    def get_image(self):
        bytes_image = config.redis.get(self.get_redis_key())
        if bytes_image is None:
            return ''
        image = image_factory.base64_to_image(bytes_image.decode())
        return image

    def get_redis_key(self):
        return 'tianhao:dark_buddy:dark_ji_word_cloud'

    def put_words(self, words):
        content = ""
        i = 0
        items = words.items()
        backitems = [[v[1], v[0]] for v in items]
        backitems.sort(reverse=True)
        for word in [backitems[i][1] for i in range(0, len(backitems))]:
            if i >= 20:
                break
            i += 1
            content += "[{0}](dtmd://dingtalkclient/sendMessage?content={1})/".format(word,quote(word))

        redis.setex(name="tianhao:dark_buddy:dark_ji_word_cloud_words", time=3600 * 12,
                    value=content[:-1])
        return content

    def get_words(self):
        words = redis.get("tianhao:dark_buddy:dark_ji_word_cloud_words")
        if words is None:
            return ""
        return words.decode()


dark_ji_word_cloud = DarkJiWordCloud()
