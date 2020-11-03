# coding=utf-8
from abc import ABCMeta, abstractmethod


class BaseHandler(metaclass=ABCMeta):
    @abstractmethod
    def do_handle(self, request_object, request_json):
        pass
