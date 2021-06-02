import json
import threading

from config import redis
from config.ChatbotsConfig import chatbots
from dark_menu.BaseHandler import BaseHandler
from dark_spy.DarkSpyGameSessionData import DarkSpyGameSessionData, GameStatusEnum, GamerRolesEnum, Gamers
from dark_spy.DarkSpyGameSessionDataEncoder import DarkSpyGameSessionDataEncoder
from lib.RandomLib import random
from lib.chatbot import ActionCard, CardItem
from mapper.DarkBuddyDarkSpyWords import select_all

gamer_icon = "{0}\t"
join_icon = "[参加](dtmd://dingtalkclient/sendMessage?content=**游戏:谁是卧底:调试:参加)\t"
start_icon = "[开始](dtmd://dingtalkclient/sendMessage?content=**游戏:谁是卧底:调试:开始)\t"
info_icon_url = "http://139.217.110.84/dark_buddy/web/darkspy/getword?chatbotUserId={0}"
hint_icon = "请讨论出投票结果后点击上面的名字\t"
vote_icon = "[{0}：{1}](dtmd://dingtalkclient/sendMessage?content=**游戏:谁是卧底:调试:投票:{0})\t"

lock = threading.Lock()


class Darkspy(BaseHandler):
    def do_handle(self, request_object, request_json):
        if request_object[2] == '开启':
            self.start_dark_spy(request_json)
            return True
        if request_object[2] == '关闭':
            self.shut_down_dark_spy(request_json)
            return True
        if request_object[2] == '调试':
            if request_object[3] == '参加':
                self.join_in(request_json)
            if request_object[3] == '开始':
                self.start_game(request_json)
            if request_object[3] == '投票':
                self.vote_player(request_object[4], request_json)
        return False

    def start_dark_spy(self, request_json):
        game_session_data = self.get_game_session_data(request_json)
        if game_session_data.game_status == GameStatusEnum.END:
            game_session_data = DarkSpyGameSessionData()
            game_session_data_str = json.dumps(game_session_data, cls=DarkSpyGameSessionDataEncoder, indent=4)
            redis.set(name=self.get_dark_spy_session_name(request_json['chatbotUserId']), value=game_session_data_str)
        self.render_game(game_session_data, request_json)

    def shut_down_dark_spy(self, request_json):
        redis.delete(self.get_dark_spy_session_name(request_json['chatbotUserId']))
        chatbots.get(request_json['chatbotUserId']).send_action_card(
            ActionCard(
                title="游戏结束",
                text="### 游戏已经回归虚无......",
                btns=[CardItem(
                    title="再来一把", url="dtmd://dingtalkclient/sendMessage?content=**游戏:谁是卧底:开启")]
            )
        )
        return

    @staticmethod
    def get_dark_spy_session_name(chatbotUserId):
        return 'tianhao:dark_buddy:dark_spy:{0}'.format(chatbotUserId)

    def build_game(self, game_session_data):
        white_word, black_word = self.build_words()
        game_session_data.white_word = white_word
        game_session_data.black_word = black_word

        gamers = game_session_data.gamers
        players_count = len(gamers)
        roles_set, white_count, black_count, fool_count = self.calculate_roles_set(players_count)
        for gamer in gamers:
            gamer.role = roles_set.pop()
        game_session_data.game_status = GameStatusEnum.GAMING
        game_session_data.result = {
            GamerRolesEnum.WHITE: white_count,
            GamerRolesEnum.BLACK: black_count,
            GamerRolesEnum.FOOL: fool_count
        }
        game_session_data.vote_info["count"] = players_count
        return game_session_data

    def build_words(self):
        total_words = select_all()
        random.shuffle(total_words)
        selected_word = random.choice(total_words)
        word_1 = selected_word.get("word_1")
        word_2 = selected_word.get("word_2")
        select_type = random.choice(['a', 'b'])
        if select_type == 'a':
            white_word = word_1
            black_word = word_2
        if select_type == 'b':
            white_word = word_2
            black_word = word_1
        return white_word, black_word

    def render_game(self, game_session_data, request_json):
        if game_session_data.game_status == GameStatusEnum.END:
            chatbots.get(request_json['chatbotUserId']).send_action_card(
                ActionCard(
                    title="游戏结束",
                    text="### 游戏已经结束......",
                    btns=[CardItem(
                        title="再来一把", url="dtmd://dingtalkclient/sendMessage?content=**游戏:谁是卧底:开启")]
                ))
        if game_session_data.game_status == GameStatusEnum.PREPARE:
            gamers = game_session_data.get_gamers()
            gamer_list = ""
            for gamer in gamers:
                gamer_list = gamer_list + gamer_icon.format(gamer.name)
            title = "暗黑卧底"
            text = '当前参与者:\t{0}\n\n{1}\n{2}'.format(gamer_list, join_icon, start_icon)
            action_card = ActionCard(title=title, text=text, btns=[])
            chatbots.get(request_json['chatbotUserId']).send_action_card(action_card)
            return
        if game_session_data.game_status == GameStatusEnum.GAMING:
            gamers = game_session_data.get_gamers()
            gamer_list = ""
            for gamer in gamers:
                if gamer.status == 0:
                    gamer_list = gamer_list + vote_icon.format(gamer.name, game_session_data.vote_info.get(gamer.name, 0))
            gamer_list = gamer_list + vote_icon.format("弃票", game_session_data.vote_info.get("弃票", 0))
            title = "暗黑卧底"
            text = '当前参与者:\t{0}\n\n{1}'.format(gamer_list, hint_icon)
            action_card = ActionCard(title=title, text=text, btns=[CardItem(title="查看你的词", url=info_icon_url.format(request_json['chatbotUserId']))])
            chatbots.get(request_json['chatbotUserId']).send_action_card(action_card)
            return
        pass

    def calculate_roles_set(self, players_count):
        result = []
        white_count = 0
        black_count = 0
        fool_count = 0
        black_num, fool_num = divmod(players_count, 3)

        if fool_num == 2:
            fool_num = 1

        for i in range(0, black_num):
            result.append(GamerRolesEnum.BLACK)
            black_count += 1

        if fool_num == 1:
            result.append(GamerRolesEnum.FOOL)
            fool_count += 1

        for i in range(0, players_count - black_num - fool_num):
            result.append(GamerRolesEnum.WHITE)
            white_count += 1
        random.shuffle(result)
        return result, white_count, black_count, fool_count

    def get_game_session_data(self, request_json):
        game_session_data = redis.get(self.get_dark_spy_session_name(request_json['chatbotUserId']))
        if game_session_data is None:
            game_session_data = DarkSpyGameSessionData()
            game_session_data = json.dumps(game_session_data, cls=DarkSpyGameSessionDataEncoder, indent=4)
            redis.setex(name=self.get_dark_spy_session_name(request_json['chatbotUserId']), time=3600,
                        value=game_session_data)
            # 参考 DarkSpyGameSessionData.decode(eval(json.dumps(game_session_data, cls=DarkSpyGameSessionDataEncoder, indent=4)))
        game_session_data = DarkSpyGameSessionData.decode(eval(game_session_data))
        return game_session_data

    def show_gamer_info(self, request_json):
        game_session_data = self.get_game_session_data(request_json)
        gamer = list(filter(lambda x: x.name == request_json['name'], game_session_data.get_gamers()))
        if not gamer:
            chatbots.get(request_json['chatbotUserId']).send_text("{0}!你还没有参加...".format(request_json['name']))
        gamer = gamer[0]
        word = ""
        if gamer.role == GamerRolesEnum.BLACK:
            word = game_session_data.black_word
        if gamer.role == GamerRolesEnum.WHITE:
            word = game_session_data.white_word
        result = {
            "name": gamer.name,
            "word": word
        }
        return result

    def join_in(self, request_json):
        game_session_data = self.get_game_session_data(request_json)
        if game_session_data.game_status == GameStatusEnum.END:
            chatbots.get(request_json['chatbotUserId']).send_text("游戏已经结束...")
            return
        if game_session_data.game_status == GameStatusEnum.GAMING:
            chatbots.get(request_json['chatbotUserId']).send_text("游戏已经开始...")
            return
        gamer = list(filter(lambda x: x.sender_id == request_json['senderId'], game_session_data.get_gamers()))
        if gamer:
            chatbots.get(request_json['chatbotUserId']).send_text("你已经参加了...")
            return
        new_gamer = Gamers()
        new_gamer.name = request_json['senderNick']
        new_gamer.sender_id = request_json['senderId']
        game_session_data.gamers.append(new_gamer)
        game_session_data_str = json.dumps(game_session_data, cls=DarkSpyGameSessionDataEncoder, indent=4)
        redis.set(name=self.get_dark_spy_session_name(request_json['chatbotUserId']), value=game_session_data_str)
        self.render_game(game_session_data, request_json)
        return

    def start_game(self, request_json):
        game_session_data = self.get_game_session_data(request_json)
        if game_session_data.game_status == GameStatusEnum.END:
            chatbots.get(request_json['chatbotUserId']).send_text("游戏已经结束...")
            return
        gamers = game_session_data.get_gamers()
        if len(gamers) < 4:
            chatbots.get(request_json['chatbotUserId']).send_text("人太少了...")
            return
        game_session_data = self.build_game(game_session_data)
        game_session_data_str = json.dumps(game_session_data, cls=DarkSpyGameSessionDataEncoder, indent=4)
        redis.set(name=self.get_dark_spy_session_name(request_json['chatbotUserId']), value=game_session_data_str)
        self.render_game(game_session_data, request_json)
        return

    def vote_player(self, player_info, request_json):
        # 暂定用名字
        game_session_data = self.get_game_session_data(request_json)
        if game_session_data.game_status == GameStatusEnum.END:
            chatbots.get(request_json['chatbotUserId']).send_text("游戏已经结束...")
            return
        if game_session_data.game_status == GameStatusEnum.PREPARE:
            chatbots.get(request_json['chatbotUserId']).send_text("游戏还未开始...")
            return
        result = game_session_data.result
        operator_player_list = list(filter(lambda x: x.name == request_json["senderNick"], game_session_data.get_gamers()))
        if not operator_player_list or operator_player_list[0].status == 1:
            chatbots.get(request_json['chatbotUserId']).send_text("{0}!你别闹！...".format(request_json["senderNick"]))
            return
        if operator_player_list[0].voted == 1:
            chatbots.get(request_json['chatbotUserId']).send_text("{0}!你都投过了！...".format(request_json["senderNick"]))
            return

        # 先处理票数
        if player_info == "弃票":
            voted_player_name = player_info
        else:
            voted_player_list = list(filter(lambda x: x.name == player_info, game_session_data.get_gamers()))
            if not voted_player_list:
                chatbots.get(request_json['chatbotUserId']).send_text("{0}!你投你🐎呢！...".format(request_json["senderNick"]))
                return
            voted_player = voted_player_list[0]
            voted_player_name = voted_player.name
        if not game_session_data.vote_info.get(voted_player_name):
            game_session_data.vote_info[voted_player_name] = 1
        else:
            game_session_data.vote_info[voted_player_name] += 1
        operator_player_list[0].voted = 1
        game_session_data.vote_info["count"] -= 1
        if game_session_data.vote_info["count"] == 0:
            game_session_data.vote_info.pop("count")
            vote_list = sorted(game_session_data.vote_info.items(), key=lambda x: x[1], reverse=True)
            if len(vote_list) > 1 and vote_list[0][1] == vote_list[1][1]:
                chatbots.get(request_json['chatbotUserId']).send_text("{0} 和 {1} 你们平票了，再battle一波吧！".format(vote_list[0][0], vote_list[1][0]))
                game_session_data.vote_info = {}
                sum = 0
                for count in result.items():
                    sum = sum + count[1]
                game_session_data.vote_info["count"] = sum
            elif len(vote_list) == 0:
                chatbots.get(request_json['chatbotUserId']).send_text("都弃票了？！再来一轮！")
                game_session_data.vote_info = {}
                sum = 0
                for count in result.items():
                    sum = sum + count[1]
                game_session_data.vote_info["count"] = sum
            else:
                voted_player = list(filter(lambda x: x.name == vote_list[0][0], game_session_data.get_gamers()))[0]
                chatbots.get(request_json['chatbotUserId']).send_text(
                    "{0}出局！！".format(voted_player.name))
                voted_player.status = 1
                result[voted_player.role] = result.get(voted_player.role) - 1
                game_winner = self.check_result(result)
                if game_winner:
                    winner_players = list(filter(lambda x: x.role == game_winner, game_session_data.get_gamers()))
                    winner_players_name = list(map(lambda x: x.name, winner_players))
                    chatbots.get(request_json['chatbotUserId']).send_text("{0}获胜！获胜者：{1}".format(game_winner, str(winner_players_name)))
                    game_session_data.game_status = GameStatusEnum.END
                game_session_data.vote_info = {}
                sum = 0
                for count in result.items():
                    sum = sum + count[1]
                game_session_data.vote_info["count"] = sum
                for gamer in game_session_data.get_gamers():
                    gamer.voted = 0
        game_session_data_str = json.dumps(game_session_data, cls=DarkSpyGameSessionDataEncoder, indent=4)
        redis.set(name=self.get_dark_spy_session_name(request_json['chatbotUserId']), value=game_session_data_str)
        self.render_game(game_session_data, request_json)
        pass

    def check_result(self, result):
        sum = 0
        for count in result.items():
            sum = sum + count[1]
        if sum != 2:
            if result.get(GamerRolesEnum.FOOL) == 0 and result.get(GamerRolesEnum.BLACK) == 0:
                return GamerRolesEnum.WHITE
            elif result.get(GamerRolesEnum.FOOL) == 0 and result.get(GamerRolesEnum.BLACK) == result.get(GamerRolesEnum.WHITE):
                return GamerRolesEnum.BLACK
            else:
                return None
        if result.get(GamerRolesEnum.FOOL) == 1:
            return GamerRolesEnum.FOOL
        if result.get(GamerRolesEnum.BLACK) >= 1:
            return GamerRolesEnum.BLACK
        return GamerRolesEnum.WHITE


dark_spy = Darkspy()
