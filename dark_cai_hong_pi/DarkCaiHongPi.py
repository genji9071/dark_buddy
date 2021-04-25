from config.ChatbotsConfig import chatbots
from dark_menu.BaseHandler import BaseHandler
from lib.RandomLib import random
from mapper.DarkBuddySweetTalk import select_by_user_id
from mapper.DarkBuddyUser import select_by_senderId


class DarkCaiHongPi(BaseHandler):
    def do_handle(self, request_object, request_json):
        self.get_cai_hong_pi_by_user_id(request_json)
        return True

    def get_cai_hong_pi_by_user_id(self, request_json):
        do_api = random.random() > 0.7
        if do_api:
            self.let_api_do(request_json)
        else:
            sender = select_by_senderId(request_json['senderId'])
            user_id = sender['id']
            records = select_by_user_id(user_id)
            if len(records) == 0:
                self.let_api_do(request_json)
            else:
                record = random.choice(records)
                str = '远哥拍了拍{0}的头，说:{1}'.format(sender['name'], record['sweet_talk'])
                chatbots.get(request_json['chatbotUserId']).send_text(str)

    def let_api_do(self, request_json):
        from juhe_api.JuheApi import juhe_api
        juhe_api.get_request('sweet', request_json)


dark_cai_hong_pi = DarkCaiHongPi()