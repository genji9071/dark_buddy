#!/usr/bin/python
# -*- coding: UTF-8 -*-
import uuid

from config import redis, now_date, public_ip
from config.ChatbotsConfig import chatbots
from dark_menu.BaseHandler import BaseHandler
from lib.chatbot import CardItem, ActionCard
from mapper.DarkBuddyMessageRecord import insert_message_record
from mapper.DarkBuddyUser import update_user, select_by_senderId
from mapper.DarkBuddyUserStatus import update_user_status, select_by_statusId_and_userId


class User_login(BaseHandler):

    def record_words(self, word, user_id):
        if word.strip():
            message_record = {
                'user_id': user_id,
                'message': word.strip()
            }
            insert_message_record(message_record)

    def login(self, json):
        user = {
            'sender_id': json['senderId'],
            'name': json['senderNick'],
            'status': 0
        }
        update_user(user)
        founded_user = select_by_senderId(json['senderId'])
        if founded_user.get('banned_time') and founded_user.get('banned_time') > now_date.now():
            chatbots.get(json['chatbotUserId']).send_text(
                "{0}，你被禁言了！解禁时间：{1}".format(json['senderNick'], founded_user.banned_time))
            return None
        return founded_user

    def do_handle(self, request_object, request_json):
        sender_id = request_json['senderId']
        sender_nick = request_json['senderNick']
        redis.setex(name=self.get_sign_in_lock_name(
            sender_id), time=60, value=sender_nick)
        btns = []
        btn = CardItem(
            title='点击注册',
            url='http://{2}/dark_buddy/web/bindid/{0}?uuid={1}'.format(sender_id, uuid.uuid1(), public_ip))
        btns.append(btn)
        title = "欢迎注册"
        text = "# {0}你好, 请点击下方按钮注册。".format(sender_nick)
        action_card = ActionCard(
            title=title, text=text, btns=btns, btn_orientation=1)
        chatbots.get(request_json['chatbotUserId']).send_action_card(action_card)

    def check_lock(self, sender_id):
        if redis.get(self.get_sign_in_lock_name(sender_id=sender_id)) is not None:
            redis.delete(self.get_sign_in_lock_name(sender_id=sender_id))
            return True
        else:
            return False

    def get_sign_in_lock_name(self, sender_id):
        return 'tianhao:dark_buddy:sign_in_lock:{0}'.format(sender_id)

    def get_temp_user_money_name(self, sender_id):
        return 'tianhao:dark_buddy:user_temp_money:{0}'.format(sender_id)

    def init_luck_point_4_temp_user(self, count, sender_id):
        redis.setex(name=self.get_temp_user_money_name(
            sender_id), time=3600, value=count)

    def give_the_lucky_point_to(self, count, sender_id):
        founded_luck_point = self.get_luck_point_by_sender_id(sender_id)
        if sender_id.startswith('/dark_buddy#'):
            redis.setex(name=self.get_temp_user_money_name(
                sender_id), time=3600, value=founded_luck_point['value'] + count)
        else:
            user_status = {'status_id': 2, 'status_code': 'luck_point', 'user_id': founded_luck_point['user_id'],
                           'value': founded_luck_point['value'] + count}
            update_user_status(user_status)

    def rewards_to_sender_id(self, count, request_json):
        self.rewards(count, request_json['senderId'], chatbots.get(request_json['chatbotUserId']),
                     request_json['senderNick'])

    def rewards(self, count, sender_id, chatbot, sender_nick):
        self.give_the_lucky_point_to(count, sender_id)
        chatbot.send_action_card(ActionCard(
            title="财富变动",
            text='### 「{0}」{1}{2}金币！'.format(sender_nick, '获得' if count > 0 else '失去', abs(count)),
            btns=[CardItem(
                title="查看当前金币剩余", url="dtmd://dingtalkclient/sendMessage?content=**人设:显示:金币")]
        ))

    def get_luck_point_by_sender_id(self, sender_id: str):
        if sender_id.startswith('/dark_buddy#'):
            return {'user_id': -1, 'value': int(redis.get(self.get_temp_user_money_name(sender_id)))}
        founded_user = select_by_senderId(sender_id)
        number = select_by_statusId_and_userId(
            2, founded_user["id"]).value
        if not number:
            number = 0
        else:
            number = int(number)
        return {'user_id': founded_user["id"], 'value': number}


user_login = User_login()
