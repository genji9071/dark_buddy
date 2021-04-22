from dark_listener.BaseListener import BaseListener
from dark_maze.DarkMaze import DarkMaze


class DarkMazeListener(BaseListener):
    def get_task_function(self):
        game_process = DarkMaze(self.user_id, self.chatbot_user_id, self)
        return game_process.start_dark_maze