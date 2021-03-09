import uuid
from threading import Thread

from config.ChatbotsConfig import chatbots
from dark_listener.BaseListener import BaseListener
from dark_show_hand.desk.GameProcess import GameProcess


class DarkShowHandListener(BaseListener):
    LISTENER_NAME = 'DarkShowHandListener'

    def initialize(self):
        self.task.start()
        pass

    def get_listener_name(self) -> str:
        return DarkShowHandListener.LISTENER_NAME

    def __init__(self, request_json: dict):
        super().__init__(request_json)
        self.game_process = GameProcess(uuid.uuid1(), self.user_id, chatbots.get(self.chatbot_user_id), self.condition,
                                        self)
        self.task = Thread(target=self.game_process.main_process)
