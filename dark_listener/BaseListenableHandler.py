# coding=utf-8
from abc import abstractmethod

from dark_listener.DarkListenerManager import DarkListenerManager
from dark_menu.BaseHandler import BaseHandler


class BaseListenableHandler(BaseHandler):

    def __init__(self, listener_name: str, listener_manager: DarkListenerManager = None):
        if listener_manager is not None:
            self.listener_manager = listener_manager
        else:
            self.listener_manager = DarkListenerManager(listener_name)

    @abstractmethod
    def do_handle(self, request_object, request_json):
        pass
