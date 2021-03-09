# coding=utf-8
import threading
from abc import ABCMeta, abstractmethod

from config import redis
from config.ChatbotsConfig import chatbots
from dark_listener.BaseOperation import validate


class BaseListener(metaclass=ABCMeta):
    LISTENER_NAME = 'base_listener'

    def __init__(self, request_json: dict):
        self.user_id = request_json['senderId']
        self.chatbot_user_id = request_json['chatbotUserId']
        self.condition = threading.Condition()
        self.current_request = request_json
        self.current_answer = None
        self.alive = True
        from dark_listener.DarkListener import dark_listeners
        dark_listeners.put(request_json, self)

    @abstractmethod
    def get_listener_name(self) -> str:
        return BaseListener.LISTENER_NAME

    def do_listen(self, request_json: dict) -> bool:
        answer = request_json["text"]["content"].strip()
        listen_words = self.get_listener_session_choices()
        if not listen_words:
            return False
        matched = validate(answer, listen_words)
        if matched:
            self.current_request = request_json
            self.current_answer = answer
            with self.condition:
                self.condition.notify()
                return True
        else:
            return False

    def destroy(self):
        redis.delete(self.get_dark_listener_session_name())
        self.alive = False
        pass

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

    def get_listener_session_choices(self):
        choices = redis.get(self.get_dark_listener_session_name())
        if not choices:
            return None
        return eval(redis.get(self.get_dark_listener_session_name()).decode())

    def is_alive(self):
        return self.alive
