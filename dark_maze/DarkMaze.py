# coding=utf-8
import uuid

import config
from config import redis
from config.ChatbotsConfig import chatbots
from dark_maze.DarkMazeListener import DarkMazeListener
from dark_maze.MazeBuilder import MazeBuilder
from dark_maze.MazePainter import maze_painter
from dark_menu.BaseHandler import BaseHandler
from lib.chatbot import ActionCard
from user.login.User_login import user_login


class DarkMaze(BaseHandler):

    def __init__(self):
        self.maze_row = 14
        self.maze_col = 14
        self.maze_type = 0
        self.sight = 2
        self.listener = None

    def start_dark_maze(self, request_json):
        if redis.get(self.get_dark_maze_session_name(request_json['chatbotUserId'])) is None:
            chatbots.get(request_json['chatbotUserId']).send_text('正在生成迷宫......')
            maze_session_data = self.build_maze()
            chatbots.get(request_json['chatbotUserId']).send_text('正在生成人物......')
            redis.setex(name=self.get_dark_maze_session_name(request_json['chatbotUserId']), time=3600, value=str(maze_session_data))
            self.listener = DarkMazeListener(request_json)
        self.treat_maze(' ', request_json=request_json)
        return

    @staticmethod
    def get_dark_maze_session_name(chatbotUserId):
        return 'tianhao:dark_buddy:dark_maze:{0}'.format(chatbotUserId)

    def shut_down_dark_maze(self, request_json):
        redis.delete(self.get_dark_maze_session_name(request_json['chatbotUserId']))
        chatbots.get(request_json['chatbotUserId']).send_text('迷宫已经回归虚无......')
        return

    def do_handle(self, request_object, request_json):
        if request_object[2] == '行动':
            if len(request_object) > 3:
                step = request_object[3]
                self.treat_maze(step, request_json=request_json)
            else:
                self.treat_maze(' ', request_json=request_json)
            return True
        if request_object[2] == '开启':
            self.start_dark_maze(request_json)
            return True
        if request_object[2] == '关闭':
            self.shut_down_dark_maze(request_json)
            return True
        return False

    def build_maze(self):
        map = {}
        if self.maze_type == 0:
            map = MazeBuilder.build_prime_maze(self.maze_row, self.maze_col)
        if self.maze_type == 1:
            map = MazeBuilder.build_tortuous_maze(self.maze_row, self.maze_col)
        player = {"location": [0, 0]}
        data = {
            "player": player,
            "map": map
        }
        return data

    def treat_maze(self, steps, request_json):
        maze_data = redis.get(self.get_dark_maze_session_name(request_json['chatbotUserId']))
        if maze_data is None:
            chatbots.get(request_json['chatbotUserId']).send_text('你要不先对我说：**游戏:迷宫:开启')
            return
        data = eval(redis.get(self.get_dark_maze_session_name(request_json['chatbotUserId'])).decode())
        preview_location = data['player']['location']
        map_location_data = data['map'][preview_location[0]][preview_location[1]]
        for step in steps:
            if step == 'a':
                if map_location_data[0] == 0 or preview_location[1] == 0:
                    self.display_maze(data, message='那是一条死路诶...', request_json=request_json)
                    return
                preview_location[1] = preview_location[1] - 1
                map_location_data = data['map'][preview_location[0]][preview_location[1]]
            elif step == 'w':
                if map_location_data[1] == 0 or preview_location[0] == 0:
                    self.display_maze(data, message='那是一条死路诶...', request_json=request_json)
                    return
                preview_location[0] = preview_location[0] - 1
                map_location_data = data['map'][preview_location[0]][preview_location[1]]
            elif step == 'd':
                if map_location_data[2] == 0 or preview_location[1] == self.maze_col - 1:
                    self.display_maze(data, message='那是一条死路诶...', request_json=request_json)
                    return
                preview_location[1] = preview_location[1] + 1
                map_location_data = data['map'][preview_location[0]][preview_location[1]]
            elif step == 's':
                if map_location_data[3] == 0 or preview_location[0] == self.maze_row - 1:
                    self.display_maze(data, message='那是一条死路诶...', request_json=request_json)
                    return
                preview_location[0] = preview_location[0] + 1
                map_location_data = data['map'][preview_location[0]][preview_location[1]]
            elif step == ' ':
                continue
        if preview_location[1] == self.maze_col - 1 and preview_location[0] == self.maze_row - 1:
            chatbots.get(request_json['chatbotUserId']).send_text('卧槽牛逼啊！这你都走出来了！')
            user_login.rewards_to_sender_id(50, request_json)
            self.shut_down_dark_maze(request_json=request_json)
            return
        self.display_maze(data, message='接下来是...', request_json=request_json)
        # 注入监听器

        return

    def display_maze(self, data, message, request_json):
        redis.set(name=self.get_dark_maze_session_name(request_json['chatbotUserId']), value=str(data))
        title = "暗黑迷宫"
        text = '![screenshot]({0})\n# {1}\n- =======[向上走](dtmd://dingtalkclient/sendMessage?content=**游戏:迷宫:行动:w)=======\n- [向左走](dtmd://dingtalkclient/sendMessage?content=**游戏:迷宫:行动:a)==[向下走](dtmd://dingtalkclient/sendMessage?content=**游戏:迷宫:行动:s)==[向右走](dtmd://dingtalkclient/sendMessage?content=**游戏:迷宫:行动:d)'.format('http://{2}/dark_buddy/dark_maze/image/get?session_id={0}&uuid={1}'.format(request_json['chatbotUserId'], uuid.uuid1(), config.public_ip), message)
        action_card = ActionCard(title=title, text=text, btns=[])
        chatbots.get(request_json['chatbotUserId']).send_action_card(action_card)
        return

    def get_maze_image(self, chatbotUserId):
        data = redis.get(self.get_dark_maze_session_name(chatbotUserId))
        if data == None:
            return
        data = eval(redis.get(self.get_dark_maze_session_name(chatbotUserId)).decode())
        return maze_painter.draw_maze(maze_data=data, horizon=self.sight, row_size=self.maze_row, col_size=self.maze_col)

dark_maze = DarkMaze()
####