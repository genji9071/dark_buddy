# coding=utf-8
from dark_guess_number.DarkGuessNumber import shut_down_guess_number
from dark_guess_number.DarkGuessNumberListener import DarkGuessNumberListener
from dark_listener.BaseListenableHandler import BaseListenableHandler


class DarkGuessNumberHandler(BaseListenableHandler):

    def initialize(self):
        super().initialize()

    def do_handle(self, request_object, request_json):
        if request_object[2] == '开启':
            self.start_game(request_json)
            return True
        if request_object[2] == '关闭':
            self.shut_down_game(request_json)
            return True
        return False

    def start_game(self, request_json):
        dark_guess_number_listener = DarkGuessNumberListener(request_json, self.listener_manager)
        self.listener_manager.put_new_listener(dark_guess_number_listener)

    def shut_down_game(self, request_json):
        user_id = request_json['senderId']
        chatbot_user_id = request_json['chatbotUserId']
        self.listener_manager.delete(user_id, chatbot_user_id)
        shut_down_guess_number(chatbot_user_id)
        pass


dark_guess_number_handler = DarkGuessNumberHandler(DarkGuessNumberListener.LISTENER_NAME)
####
