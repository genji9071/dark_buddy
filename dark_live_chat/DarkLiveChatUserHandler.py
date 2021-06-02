from config.ChatbotsConfig import chatbots
from dark_menu.BaseHandler import BaseHandler
from user.login.User_login import user_login


class DarkLiveChatUserHandler(BaseHandler):
    def do_handle(self, request_array, request_json):
        if request_array[2] == '金币':
            money = user_login.get_luck_point_by_sender_id(request_json['senderId'])['value']
            chatbots.get(request_json['chatbotUserId']).send_text(
                "当前的金币数：{0}".format(money))
            return True
        return False


dark_live_chat_user_handler = DarkLiveChatUserHandler()
