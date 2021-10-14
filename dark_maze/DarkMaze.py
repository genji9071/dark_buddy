# coding=utf-8
import uuid

import config
from config import redis
from config.ChatbotsConfig import chatbots
from dark_listener.BaseOperation import BaseSymbol, SYMBOL_MATCH
from dark_maze.MazeBuilder import MazeBuilder
from dark_maze.MazePainter import maze_painter
from lib.BaseChatbot import ActionCard
from user.login.User_login import user_login


def get_dark_maze_session_name(chatbotUserId):
    return 'tianhao:dark_buddy:dark_maze:{0}'.format(chatbotUserId)


def shut_down_dark_maze(chatbot_user_id):
    redis.delete(get_dark_maze_session_name(chatbot_user_id))
    chatbots.get(chatbot_user_id).send_text('迷宫已经回归虚无......')
    return


def get_maze_image(chatbotUserId):
    data = redis.get(get_dark_maze_session_name(chatbotUserId))
    if data is None:
        return
    data = eval(redis.get(get_dark_maze_session_name(chatbotUserId)).decode())
    return maze_painter.draw_maze(maze_data=data, horizon=sight, row_size=maze_row,
                                  col_size=maze_col)


REGEX_ANY_STEP = r'[wsadWSAD]+'

maze_operator = BaseSymbol(SYMBOL_MATCH, REGEX_ANY_STEP)

maze_row = 14

maze_col = 14

maze_type = 0

sight = 2


class DarkMaze:

    def __init__(self, user_id, chatbot_user_id, listener):
        self.maze_row = maze_row
        self.maze_col = maze_col
        self.maze_type = maze_type
        self.sight = sight
        self.user_id = user_id
        self.chatbot_user_id = chatbot_user_id
        self.listener = listener

    def start_dark_maze(self):
        if redis.get(get_dark_maze_session_name(self.chatbot_user_id)) is None:
            chatbots.get(self.chatbot_user_id).send_text('正在生成迷宫......')
            maze_session_data = self.build_maze()
            chatbots.get(self.chatbot_user_id).send_text('正在生成人物......')
            redis.setex(name=get_dark_maze_session_name(self.chatbot_user_id), time=3600,
                        value=str(maze_session_data))
        self.listener.current_answer = ' '
        while self.treat_maze(self.listener.current_answer):
            self.listener.ask(maze_operator, '输入wsad移动')
        shut_down_dark_maze(self.chatbot_user_id)

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

    def treat_maze(self, steps):
        maze_data = redis.get(get_dark_maze_session_name(self.chatbot_user_id))
        if maze_data is None:
            chatbots.get(self.chatbot_user_id).send_text('你要不先对我说：**游戏:迷宫:开启')
            return False
        data = eval(redis.get(get_dark_maze_session_name(self.chatbot_user_id)).decode())
        preview_location = data['player']['location']
        map_location_data = data['map'][preview_location[0]][preview_location[1]]
        for step in steps:
            if step == 'a':
                if map_location_data[0] == 0 or preview_location[1] == 0:
                    self.display_maze(data, message='那是一条死路诶...')
                    return True
                preview_location[1] = preview_location[1] - 1
                map_location_data = data['map'][preview_location[0]][preview_location[1]]
            elif step == 'w':
                if map_location_data[1] == 0 or preview_location[0] == 0:
                    self.display_maze(data, message='那是一条死路诶...')
                    return True
                preview_location[0] = preview_location[0] - 1
                map_location_data = data['map'][preview_location[0]][preview_location[1]]
            elif step == 'd':
                if map_location_data[2] == 0 or preview_location[1] == self.maze_col - 1:
                    self.display_maze(data, message='那是一条死路诶...')
                    return True
                preview_location[1] = preview_location[1] + 1
                map_location_data = data['map'][preview_location[0]][preview_location[1]]
            elif step == 's':
                if map_location_data[3] == 0 or preview_location[0] == self.maze_row - 1:
                    self.display_maze(data, message='那是一条死路诶...')
                    return True
                preview_location[0] = preview_location[0] + 1
                map_location_data = data['map'][preview_location[0]][preview_location[1]]
            elif step == ' ':
                continue
        if preview_location[1] == self.maze_col - 1 and preview_location[0] == self.maze_row - 1:
            chatbots.get(self.chatbot_user_id).send_text('卧槽牛逼啊！这你都走出来了！')
            user_login.rewards(50, self.user_id, chatbots.get(self.chatbot_user_id), '')
            return False
        self.display_maze(data, message='接下来是...')
        return True

    def display_maze(self, data, message):
        redis.set(name=get_dark_maze_session_name(self.chatbot_user_id), value=str(data))
        title = "暗黑迷宫"
        img_url = 'http://{2}/dark_buddy/dark_maze/image/get?session_id={0}&uuid={1}'.format(self.chatbot_user_id,
                                                                                             uuid.uuid1(),
                                                                                             config.public_ip)
        text = '![screenshot]({0})\n# {1}'.format(img_url, message)
        action_card = ActionCard(title=title, text=text, btns=[], img_url=img_url)
        chatbots.get(self.chatbot_user_id).send_action_card(action_card)
        return
