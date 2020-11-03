from dark_show_hand.ai.AnalysisFace import judge
from dark_show_hand.desk.Bet import Bet
from dark_show_hand.desk.Draw import Draw


class GameProcess:
    def __init__(self, id, player_id, chatbot, condition, listener):
        self.id = id
        self.player_id = player_id
        self.draw = Draw()
        self.bet = Bet(player_id, chatbot, listener)
        self.condition = condition
        self.listener = listener

    def main_process(self):
        self.bet.init_bet()
        self.draw.draw(is_hidden=True)
        showed_hand = False
        for turn in [1, 2, 3, 4]:
            player_card, ai_card = self.draw.draw(is_hidden=False)
            if showed_hand:
                continue
            self.render_cards()
            bet_result = self.bet.bet(start_from='ai' if ai_card.bigger_than(player_card) else 'player', draw=self.draw)
            if bet_result == 'ok':
                continue
            if bet_result == 'ai_give_up':
                self.bet.win(self.player_id, self.bet.ai_bet + self.bet.player_bet)
                return
            if bet_result == 'player_give_up':
                self.bet.lose(self.player_id)
                return
            if bet_result == 'player_show_hand':
                showed_hand = True
                continue
        player_cards = self.draw.player_cards
        ai_cards = self.draw.ai_cards
        judgement = judge(player_cards, ai_cards)
        self.render_cards(is_final=True)
        if judgement == 0:
            # 玩家获胜
            self.bet.win(self.player_id, self.bet.ai_bet + self.bet.player_bet)
        else:
            self.bet.lose(self.player_id)
        self.listener.destroy()

    def render_cards(self, is_final=False):
        player_cards = self.draw.player_cards
        ai_cards = self.draw.ai_cards
        player_cards_str = []
        ai_cards_str = []
        for card in player_cards:
            player_cards_str.append(card['card'].describe())
        for card in ai_cards:
            if card['is_hidden'] and not is_final:
                ai_cards_str.append("??")
            else:
                ai_cards_str.append(card['card'].describe())
        text = "# 你的牌：\n {0}\n # AI的牌：\n {1} \n## 桌上金币：${2}".format(player_cards_str, ai_cards_str,
                                                                    self.bet.ai_bet + self.bet.player_bet)
        self.bet.chatbot.send_markdown(title="猜数字", text=text)
