# coding=utf-8
from dark_listener.BaseListenableHandler import BaseListenableHandler
from dark_work_shuang_rank.DarkWorkShuangRankListener import DarkWorkShuangRankListener, shut_down_work_shuang_rank

LISTENER_NAME = 'DarkWorkShuangRankListener'


class DarkWorkShuangRankHandler(BaseListenableHandler):

    def do_handle(self, request_object, request_json):
        if request_object[1] == '开启':
            self.start_test(request_json)
            return True
        if request_object[1] == '关闭':
            self.shut_down_test(request_json)
            return True
        return False

    def start_test(self, request_json):
        dark_work_shuang_rank_listener = DarkWorkShuangRankListener(request_json, self.listener_manager)
        self.listener_manager.put_new_listener(dark_work_shuang_rank_listener)

    def shut_down_test(self, request_json):
        user_id = request_json['senderId']
        chatbot_user_id = request_json['chatbotUserId']
        self.listener_manager.delete(user_id, chatbot_user_id)
        shut_down_work_shuang_rank(chatbot_user_id)
        pass


dark_work_shuang_rank = DarkWorkShuangRankHandler(LISTENER_NAME)
####
