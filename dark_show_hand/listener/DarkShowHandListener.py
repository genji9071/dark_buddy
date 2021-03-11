import uuid

from config.ChatbotsConfig import chatbots
from dark_listener.BaseListener import BaseListener
from dark_show_hand.desk.GameProcess import GameProcess


class DarkShowHandListener(BaseListener):

    def get_task_function(self):
        self.game_process = GameProcess(uuid.uuid1(), self.user_id, chatbots.get(self.chatbot_user_id), self)
        return self.game_process.main_process

    LISTENER_NAME = 'DarkShowHandListener'

    def get_listener_name(self) -> str:
        return DarkShowHandListener.LISTENER_NAME
