from config.ChatbotsConfig import chatbots
from dark_listener.BaseListenableHandler import BaseListenableHandler
from dark_show_hand.desk.Bet import Bet
from dark_twenty_one.DarkTwentyOneListener import DarkTwentyOneListener
from user.login.User_login import user_login

LISTENER_NAME = 'DarkTwentyOneListener'


class DarkTwentyOneHandler(BaseListenableHandler):

    def initialize(self):
        super().initialize()

    def do_handle(self, request_object, request_json):
        if '来一把' in request_object[2]:
            self.start_the_game(request_json)
            return True
        if '掀桌子' in request_object[2]:
            self.fuck_the_game(request_json)
            return True
        return False

    def start_the_game(self, request_json):
        money = user_login.get_luck_point_by_sender_id(request_json['senderId'])['value']
        if money < Bet.minimum_init_bet:
            chatbots.get(request_json['chatbotUserId']).send_text("100金币开局，没钱你还是先靠边站吧...")
            return
        dark_21_listener = DarkTwentyOneListener(request_json, self.listener_manager)
        self.listener_manager.put_new_listener(dark_21_listener)

    def fuck_the_game(self, request_json):
        user_id = request_json['senderId']
        chatbot_user_id = request_json['chatbotUserId']
        self.listener_manager.delete(user_id, chatbot_user_id)
        chatbots.get(request_json['chatbotUserId']).send_text("桌子掀了...")


dark_twenty_one = DarkTwentyOneHandler(LISTENER_NAME)
