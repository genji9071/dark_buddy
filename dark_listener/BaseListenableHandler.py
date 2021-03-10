# coding=utf-8
from abc import abstractmethod

from dark_listener.BaseOperation import BaseOperator, build_mock_operator
from dark_listener.DarkListenerManager import DarkListenerManager
# 场景开始，迭代器的头部必须以此开始
from dark_menu.BaseHandler import BaseHandler

PHASE_START = 'PHASE_START'

# 场景结束，handler不再进行监听，全局结束
PHASE_END = 'PHASE_END'


class ListenableHandlerPhase:

    def __init__(self, phase_id: str, phase_description: str, phase_listener_operation: BaseOperator):
        # id唯一，用来区分不同场景下的提问
        self.phase_id = phase_id
        # 描述，机器的问题，可以为空（误
        self.phase_description = phase_description
        # 捕捉的规则
        self.phase_listener_operation = phase_listener_operation


class BaseListenableHandler(BaseHandler):

    def make_listenable_handler_phase(self, phase_id: str, phase_description: str,
                                      phase_listener_operation: BaseOperator) -> ListenableHandlerPhase:
        if phase_id in self.__phase_map__:
            raise ValueError(f"已经存在phase_id为{phase_id}的场景。")
        new_phase = ListenableHandlerPhase(phase_id, phase_description, phase_listener_operation)
        self.__phase_map__.setdefault(phase_id, new_phase)
        return new_phase

    def __init__(self, listener_name: str, listener_manager: DarkListenerManager = None):
        if listener_manager is not None:
            self.listener_manager = listener_manager
        else:
            self.listener_manager = DarkListenerManager(listener_name)
        self.__phase_map__ = {}
        self.initialize()
        # 类构成检查
        if PHASE_START not in self.__phase_map__:
            raise ValueError(f"handler 初始化异常，找不到phase_id为{PHASE_START}的场景。")
        if PHASE_END not in self.__phase_map__:
            raise ValueError(f"handler 初始化异常，找不到phase_id为{PHASE_END}的场景。")

    def get_phase_by_phase_id(self, phase_id: str):
        if phase_id not in self.__phase_map__:
            raise ValueError(f"找不到phase_id为{phase_id}的场景。")
        return self.__phase_map__.get(phase_id)

    @abstractmethod
    def do_handle(self, request_object, request_json):
        pass

    @abstractmethod
    def initialize(self):
        # 实现phase_map的封装，调用方法make_listenable_handler_phase
        self.build_mock_phase_start()
        self.build_mock_phase_end()
        pass

    def build_mock_phase_start(self):
        self.make_listenable_handler_phase(PHASE_START, "MOCK PHASE START", build_mock_operator())

    def build_mock_phase_end(self):
        self.make_listenable_handler_phase(PHASE_END, "MOCK PHASE END", build_mock_operator())
