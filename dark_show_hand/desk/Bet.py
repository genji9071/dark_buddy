import eventlet

from dark_listener.BaseOperation import BaseOperator, OPERATOR_OR, BaseSymbol, SYMBOL_EQUALS, SYMBOL_MATCH, \
    REGEX_ANY_NUMBER
from dark_show_hand.ai.Ai import Ai
from dark_show_hand.desk.Draw import Draw
from lib.chatbot import ActionCard, CardItem
from user.login.User_login import user_login

bet_operation = BaseOperator(OPERATOR_OR, [BaseSymbol(SYMBOL_EQUALS, 'giveup'),
                                           BaseSymbol(SYMBOL_MATCH, REGEX_ANY_NUMBER)])

class Bet:
    minimum_per_bet = 10
    minimum_init_bet = 100
    maximum_per_bet = 10000

    def __init__(self, player_id, chatbot, listener):
        self.ai = Ai(self)
        self.player_id = player_id
        self.chatbot = chatbot
        self.listener = listener
        self.player_bet = 0
        self.ai_bet = 0

    def init_bet(self):
        self.ai_bet += Bet.minimum_init_bet
        self.push_money(Bet.minimum_init_bet)

    def win(self, player_id, total_money):
        self.chatbot.send_action_card(ActionCard(
            title="暗黑梭哈",
            text="### 你赢了！「{0}」金币都是你的！".format(total_money),
            btns=[CardItem(
                title="再来一把", url="dtmd://dingtalkclient/sendMessage?content=**游戏:暗黑梭哈:来一把")]
        ))
        user_login.rewards(total_money, player_id, self.chatbot, '玩家')

    def lose(self, player_id):
        self.chatbot.send_action_card(ActionCard(
            title="暗黑梭哈",
            text="### 你输了！呵呵...",
            btns=[CardItem(
                title="再来一把", url="dtmd://dingtalkclient/sendMessage?content=**游戏:暗黑梭哈:来一把")]
        ))

    def bet(self, start_from, draw: Draw, order=None) -> str:
        # 返回值：
        # 'ok' 双方完成bet
        # 'ai_give_up' ai放弃
        # 'player_give_up' 玩家放弃
        # 'player_show_hand' 玩家梭哈
        if start_from == 'ai':
            ai_bet_result = self.ai.think(draw, order)
            if ai_bet_result['bet_type'] == 'ai_give_up':
                return 'ai_give_up'
            self.ai_bet += ai_bet_result['bet_count']
            if self.player_bet == self.ai_bet:
                return 'ok'
            player_bet_result = self.ask_for_bet(ai_bet_result['bet_count'])
            if player_bet_result['bet_type'] == 'player_give_up':
                return 'player_give_up'
            self.push_money(player_bet_result['bet_count'])
            if player_bet_result['bet_type'] == 'player_show_hand':
                ai_bet_result = self.ai.think_show_hand(draw, order)
                if ai_bet_result['bet_type'] == 'ai_give_up':
                    return 'ai_give_up'
                self.ai_bet = self.player_bet
                return 'player_show_hand'
            if self.player_bet > self.ai_bet:
                return self.bet('ai', draw, player_bet_result['bet_count'])
        else:
            player_bet_result = self.ask_for_bet(order)
            if player_bet_result['bet_type'] == 'player_give_up':
                return 'player_give_up'
            self.push_money(player_bet_result['bet_count'])
            if player_bet_result['bet_type'] == 'player_show_hand':
                ai_bet_result = self.ai.think_show_hand(draw, order)
                if ai_bet_result['bet_type'] == 'ai_give_up':
                    return 'ai_give_up'
                self.ai_bet = self.player_bet
                return 'player_show_hand'
            if self.player_bet == self.ai_bet:
                return 'ok'
            ai_bet_result = self.ai.think(draw, player_bet_result['bet_count'])
            if ai_bet_result['bet_type'] == 'ai_give_up':
                return 'ai_give_up'
            self.ai_bet += ai_bet_result['bet_count']
            if self.ai_bet > self.player_bet:
                return self.bet('player', draw, order)
        return 'ok'

    def ask_for_bet(self, ai_order=None) -> dict:
        # bet_type: 下注类型
        # 'normal' 常规下注
        # 'player_give_up' 玩家放弃
        # 'player_show_hand' 玩家梭哈
        # bet_count：下注金额
        result = {
            'bet_type': 'normal',
            'bet_count': 0
        }
        prefix = '由你开始下注。'
        minimum = Bet.minimum_per_bet
        if ai_order:
            prefix = 'AI下注了{0}个金币。'.format(ai_order)
            minimum = self.ai_bet - self.player_bet
        bet_money = self.listener.ask(bet_operation, '{0}请输入金额，不少于{1}块，或者输入giveup放弃，颗粒无收！'.format(prefix, minimum))
        if bet_money == 'giveup':
            result['bet_type'] = 'player_give_up'
            return result
        current_money = user_login.get_luck_point_by_sender_id(self.player_id)['value']
        bet_money = int(bet_money)
        if bet_money >= current_money:
            self.chatbot.send_text('你梭哈了，当前的所有金币：「{0}」全部用于下注！'.format(current_money))
            eventlet.sleep(1)
            result['bet_type'] = 'player_show_hand'
            result['bet_count'] = current_money
        else:
            if bet_money < 10:
                self.chatbot.send_text('输入金额小于{0}，请重新输入！'.format(minimum))
                return self.ask_for_bet()
            result['bet_count'] = bet_money
        return result

    def push_money(self, count):
        self.player_bet += count
        user_login.give_the_lucky_point_to(-count, self.player_id)
