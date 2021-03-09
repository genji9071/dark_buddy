from dark_listener.BaseListener import BaseListener


class DarkMazeListener(BaseListener):
    LISTENER_NAME = 'DarkMazeListener'

    def get_listener_name(self) -> str:
        return DarkMazeListener.LISTENER_NAME
