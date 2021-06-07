# coding=utf-8
import threading
import traceback

from config import redis
from dark_listener import BaseListener
from dark_listener.BaseOperation import validate
from dark_listener.ListenerManagerLauncher import listener_manager_launcher
from lib.Logger import log

rlock = threading.RLock()


def lock(func):
    def wrapper(*args, **kwargs):
        rlock.acquire()
        try:
            return func(*args, **kwargs)
        except:
            log.error(traceback.format_exc())
            raise
        finally:
            rlock.release()

    return wrapper


class DarkListenerManager():
    def __init__(self, listener_name):
        self.listener_name = listener_name
        self.listeners = {}

    def get_dark_listener_session_name(self, user_id: str, chatbot_user_id: str):
        return 'tianhao:dark_buddy:dark_listener:{0}:{1}'.format(self.listener_name,
                                                                 user_id + '-*-' + chatbot_user_id)

    def get_listener_session_choices(self, user_id: str, chatbot_user_id: str):
        choices = redis.get(self.get_dark_listener_session_name(user_id, chatbot_user_id))
        if not choices:
            return None
        return eval(redis.get(self.get_dark_listener_session_name(user_id, chatbot_user_id)).decode())

    def clear_listener_session_choices(self, user_id: str, chatbot_user_id: str):
        redis.delete(self.get_dark_listener_session_name(user_id, chatbot_user_id))

    @lock
    def put_new_listener(self, dark_listener: BaseListener) -> None:
        tenant_id = dark_listener.chatbot_user_id
        user_id = dark_listener.user_id
        listeners_dict = self.listeners.get(tenant_id, {})
        listeners_dict[user_id] = dark_listener
        self.listeners[tenant_id] = listeners_dict
        # 注册租户当前焦点
        listener_manager_launcher.set_current_listener_manager(user_id, tenant_id, self)

    @lock
    def get_listener(self, user_id: str, tenant_id: str) -> BaseListener:
        listener_dict = self.listeners.get(tenant_id)
        if not listener_dict:
            return None
        return listener_dict.get(user_id, None)

    @lock
    def delete(self, user_id, chatbot_user_id):
        related_listener = self.get_listener(user_id, chatbot_user_id)
        if related_listener:
            redis.delete(self.get_dark_listener_session_name(user_id, chatbot_user_id))
            related_listener.alive = False
            del related_listener

    @lock
    def listen(self, request_json: dict) -> bool:
        user_id = request_json['senderId']
        chatbot_user_id = request_json['chatbotUserId']
        related_listener = self.get_listener(user_id, chatbot_user_id)
        if not related_listener:
            return False
        answer = request_json["text"]["content"].strip()
        listen_words = self.get_listener_session_choices(user_id, chatbot_user_id)
        if not listen_words:
            return False
        matched = validate(answer, listen_words)
        if matched:
            self.clear_listener_session_choices(user_id, chatbot_user_id)
            related_listener.current_request = request_json
            related_listener.current_answer = answer
            return True
        else:
            return False

    def get_listener_name(self):
        return self.listener_name
