# coding=utf-8

from dark_listener.BaseListenableHandler import BaseListenableHandler
from dark_maze.DarkMaze import shut_down_dark_maze
from dark_maze.DarkMazeListener import DarkMazeListener


class DarkMazeHandler(BaseListenableHandler):

    def initialize(self):
        super().initialize()

    def do_handle(self, request_object, request_json):
        if request_object[2] == '开启':
            self.start_dark_maze(request_json)
            return True
        if request_object[2] == '关闭':
            self.shut_down_dark_maze(request_json)
            return True
        return False

    def start_dark_maze(self, request_json):
        dark_maze_listener = DarkMazeListener(request_json, self.listener_manager)
        self.listener_manager.put_new_listener(dark_maze_listener)

    def shut_down_dark_maze(self, request_json):
        user_id = request_json['senderId']
        chatbot_user_id = request_json['chatbotUserId']
        self.listener_manager.delete(user_id, chatbot_user_id)
        shut_down_dark_maze(chatbot_user_id)
        pass


dark_maze = DarkMazeHandler(DarkMazeListener.LISTENER_NAME)
####
