from dark_listener.BaseListenableHandler import BaseListenableHandler
from dark_listener.BaseListener import BaseListener
from dark_listener.BaseOperation import build_all_accept_operator

LISTENER_NAME = 'DarkDebugListener'


class DarkDebugListener(BaseListener):

    def ask_sth(self):
        print(self.ask(build_all_accept_operator(), '测试测试测试测试测试测试测试测试'))
        print(self.listener_manager.listeners)
        pass

    def get_task_function(self):
        return self.ask_sth


class DarkDebugListenerHandler(BaseListenableHandler):

    def do_handle(self, request_object, request_json):
        listener = DarkDebugListener(request_json, self.listener_manager)
        self.listener_manager.put_new_listener(listener)
        return True


dark_debug_listener = DarkDebugListenerHandler(LISTENER_NAME)
