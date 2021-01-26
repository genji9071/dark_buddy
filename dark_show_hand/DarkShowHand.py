from config.ChatbotsConfig import chatbots
from dark_listener.DarkListener import dark_listeners
from dark_menu.BaseHandler import BaseHandler
from dark_show_hand.desk.Bet import Bet
from dark_show_hand.listener.DarkShowHandListener import DarkShowHandListener
from user.login.User_login import user_login


class DarkShowHand(BaseHandler):
    def do_handle(self, request_object, request_json):
        if '来一把' in request_object[2]:
            self.start_the_game(request_json)
            return True
        if '掀桌子' in request_object[2]:
            self.fuck_the_game(request_json)
            return True
        return False

    def start_the_game(self, request_json):
        # existed_dark_show_hand_listener = dark_listeners.get_by_listener_name(request_json,
        #                                                                       DarkShowHandListener.LISTENER_NAME)
        # if existed_dark_show_hand_listener and existed_dark_show_hand_listener.user_id != request_json['senderId']:
        #     chatbots.get(request_json['chatbotUserId']).send_text("别人的桌子已经开了，有钱你就掀TA桌子吧...")
        #     return
        money = user_login.get_luck_point_by_sender_id(request_json['senderId'])['value']
        if money < Bet.minimum_init_bet:
            chatbots.get(request_json['chatbotUserId']).send_text("100金币开局，没钱你还是先靠边站吧...")
            return
        dark_show_hand_listener = DarkShowHandListener(request_json)
        dark_listeners.put(request_json, dark_show_hand_listener)
        dark_show_hand_listener.initialize()

    def fuck_the_game(self, request_json):
        dark_listeners.delete(request_json, DarkShowHandListener.LISTENER_NAME)
        chatbots.get(request_json['chatbotUserId']).send_text("桌子掀了...")
        pass


dark_show_hand = DarkShowHand()