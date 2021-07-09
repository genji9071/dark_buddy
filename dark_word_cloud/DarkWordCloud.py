# coding=utf-8
import uuid

import config
import dark_word_cloud.CloudMaker as cloudMaker
import mapper
from config import redis
from config.ChatbotsConfig import chatbots
from dark_menu.BaseHandler import BaseHandler
from lib.BaseChatbot import ActionCard
from lib.ImageFactory import image_factory


class DarkWordCloud(BaseHandler):
    def do_handle(self, request_object, request_json):
        id = uuid.uuid1()
        image = self.get_image()
        if image == '':
            chatbots.get(request_json['chatbotUserId']).send_text('正在生成中，这可能需要一些时间...')
            image = self.get_word_cloud_image()
            self.put_image(image)
        title = "暗黑热搜"
        text = "![screenshot](http://{2}/dark_buddy/dark_word_cloud/image/get?session_id={0}&uuid={1})\n# 暗黑热搜榜".format(request_json['chatbotUserId'], id, config.public_ip)
        action_card = ActionCard(title=title, text=text, btns=[])
        chatbots.get(request_json['chatbotUserId']).send_action_card(action_card)

    @staticmethod
    def get_word_cloud_image():
        results = mapper.mapper_message_record.select_word_frequency()
        dict = {}
        for p in results:
            dict[p['message']] = p['count']
        return cloudMaker.make_word_cloud_to_image(dict)

    def put_image(self, image):
        data = image_factory.image_to_base64(image)
        redis.setex(name=self.get_redis_key(), time=3600 * 12,
                    value=data)
        return

    def get_image(self):
        bytes_image = redis.get(self.get_redis_key())
        if bytes_image is None:
            return ''
        image = image_factory.base64_to_image(bytes_image.decode())
        return image

    def get_redis_key(self):
        return 'tianhao:dark_buddy:dark_word_cloud'


dark_word_cloud = DarkWordCloud()