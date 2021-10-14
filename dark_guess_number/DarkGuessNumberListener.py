from dark_guess_number.DarkGuessNumber import DarkGuessNumber
from dark_listener.BaseListener import BaseListener


class DarkGuessNumberListener(BaseListener):
    def get_listener_task(self):
        game_process = DarkGuessNumber(self.user_id, self.chatbot_user_id, self)
        return game_process.start_guess_number()
