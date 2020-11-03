# coding=utf-8
import threading
import traceback

from dark_listener import BaseListener
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


class DarkListener():
    def __init__(self):
        self.listeners = {}

    @lock
    def put(self, request_json: dict, dark_listener: BaseListener) -> None:
        key = self.get_key_from_request_json(request_json)
        # self.listeners[key].append(dark_listener)
        listeners_dict = self.listeners.get(key, {})
        listeners_dict[request_json['senderId']] = dark_listener
        self.listeners[key] = listeners_dict

    @lock
    def get_by_listener_name(self, request_json: dict, listener_name: str) -> BaseListener:
        key = self.get_key_from_request_json(request_json)
        listener_dict = self.listeners.get(key)
        if not listener_dict:
            return None
        for listener in filter(lambda x: x.get_listener_name() == listener_name and x.is_alive(),
                               list(listener_dict.values())):
            if listener and listener.is_alive():
                return listener
            else:
                return None

    @lock
    def get_by_sender_id(self, request_json: dict):
        key = self.get_key_from_request_json(request_json)
        listener_dict = self.listeners.get(key)
        if not listener_dict:
            return None
        return listener_dict.get(request_json['senderId'], None)

    @lock
    def delete(self, request_json: dict, listener_name: str):
        related_listener = self.get_by_listener_name(request_json, listener_name)
        if related_listener:
            related_listener.destroy()
            del related_listener

    @lock
    def listen(self, request_json: dict) -> bool:
        related_listener = self.get_by_sender_id(request_json)
        if not related_listener:
            return False
        return related_listener.do_listen(request_json)

    @staticmethod
    def get_key_from_request_json(request_json: dict) -> str:
        return request_json['chatbotUserId']


dark_listeners = DarkListener()
