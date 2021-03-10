# coding=utf-8
import threading
from abc import ABCMeta, abstractmethod

from config import redis
from config.ChatbotsConfig import chatbots


class BaseListener(metaclass=ABCMeta):

    def __init__(self, request_json: dict, listener_manager):
        self.user_id = request_json['senderId']
        self.chatbot_user_id = request_json['chatbotUserId']
        self.listener_manager = listener_manager
        self.condition = threading.Condition()
        self.current_request = request_json
        self.current_answer = None
        self.alive = True

    @abstractmethod
    def get_listener_name(self) -> str:
        raise RuntimeError("Empty listener name!")

    @abstractmethod
    def initialize(self):
        raise RuntimeError("Empty initialize impl!")

    def ask(self, choices, question: str):
        self.set_listener_session_choices(choices)
        if question:
            chatbots.get(self.chatbot_user_id).send_text(question)
        with self.condition:
            self.condition.wait()
            return self.current_answer

    def get_dark_listener_session_name(self):
        return 'tianhao:dark_buddy:dark_listener:{0}:{1}'.format(self.get_listener_name(),
                                                                 self.user_id + '-*-' + self.chatbot_user_id)

    def set_listener_session_choices(self, choices):
        redis.setex(name=self.get_dark_listener_session_name(), time=3600,
                    value=str(choices))

    def is_alive(self):
        return self.alive
