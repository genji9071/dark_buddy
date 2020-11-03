class GameStatusEnum:
    PREPARE = '准备中'
    GAMING = '游戏中'
    END = '已结束'

    map = {
        '准备中': PREPARE,
        '游戏中': GAMING,
        '已结束': END
    }


class GamerRolesEnum:
    WHITE = '平民'
    BLACK = '卧底'
    FOOL = '白板'
    UNKNOWN = '未知'

    map = {
        '平民': WHITE,
        '卧底': BLACK,
        '白板': FOOL,
        '未知': UNKNOWN
    }


class Gamers:
    def __init__(self):
        self.name = '一个玩家'
        self.sender_id = '玩家id'
        self.token = '玩家token'
        self.role = GamerRolesEnum.UNKNOWN
        self.status = 0
        self.voted = 0

    def encode(self):
        return {
            "name": self.name,
            "sender_id": self.sender_id,
            "token": self.token,
            "role": self.role,
            "status": self.status,
            "voted": self.voted
        }

    @classmethod
    def decode(self, dict):
        gamer = Gamers()
        gamer.name = dict.get("name")
        gamer.sender_id = dict.get("sender_id")
        gamer.token = dict.get("token")
        gamer.status = dict.get("status")
        gamer.role = dict.get("role")
        gamer.voted = dict.get("voted")
        return gamer

class DarkSpyGameSessionData():
    def __init__(self):
        self.game_status = GameStatusEnum.PREPARE
        self.gamers = []
        self.white_word = ""
        self.black_word = ""
        self.result = {}
        self.vote_info = {}

    def get_gamers(self):
        return self.gamers

    @classmethod
    def decode(self, dict):
        data = DarkSpyGameSessionData()
        data.game_status = dict.get("game_status")
        data.white_word = dict.get("white_word")
        data.black_word = dict.get("black_word")
        data.result = dict.get("result")
        data.vote_info = dict.get("vote_info")
        data.gamers = list(map(lambda x: Gamers.decode(x), dict.get("gamers")))
        return data
