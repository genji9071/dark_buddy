import json

from dark_spy.DarkSpyGameSessionData import DarkSpyGameSessionData


class DarkSpyGameSessionDataEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, DarkSpyGameSessionData):
            return {
                'game_status': obj.game_status,
                'white_word': obj.white_word,
                'black_word': obj.black_word,
                'result': obj.result,
                'gamers': list(map(lambda x: x.encode(), obj.gamers)),
                'vote_info': obj.vote_info
            }
        return json.JSONEncoder.default(self, obj)