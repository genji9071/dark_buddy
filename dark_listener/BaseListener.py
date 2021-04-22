# coding=utf-8
from abc import ABCMeta, abstractmethod

import eventlet

from config import redis
from config.ChatbotsConfig import chatbots
from dark_live_chat import socketio


class BaseListener(metaclass=ABCMeta):

    def __init__(self, request_json: dict, listener_manager):
        self.user_id = request_json['senderId']
        self.chatbot_user_id = request_json['chatbotUserId']
        self.listener_manager = listener_manager
        self.current_request = request_json
        self.current_answer = None

    def get_listener_name(self) -> str:
        return self.listener_manager.LISTENER_NAME

    @abstractmethod
    def get_task_function(self):
        raise RuntimeError("Empty task define!")

    def initialize(self):
        task = self.get_task_function()
        if not hasattr(task, '__call__'):
            raise RuntimeError("task is not callable!")
        socketio.start_background_task(target=task)

    def ask(self, choices, question: str):
        self.current_answer = None
        self.set_listener_session_choices(str(choices.encode()))
        if question:
            chatbots.get(self.chatbot_user_id).send_text(question)
        while self.current_answer is None:
            eventlet.sleep(1)
        return self.current_answer

    def get_dark_listener_session_name(self):
        return 'tianhao:dark_buddy:dark_listener:{0}:{1}'.format(self.get_listener_name(),
                                                                 self.user_id + '-*-' + self.chatbot_user_id)

    def set_listener_session_choices(self, choices):
        redis.setex(name=self.get_dark_listener_session_name(), time=3600,
                    value=str(choices))
