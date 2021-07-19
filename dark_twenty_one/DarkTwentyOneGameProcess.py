import eventlet

from dark_twenty_one.ai import Ai
from dark_twenty_one.desk.BasicDraw import BasicDraw
from lib.BaseChatbot import ActionCard, CardItem
from user.login.User_login import user_login


class DarkTwentyOneGameProcess():
    def __init__(self, id, player_id, chatbot, listener):
        self.id = id
        self.player_id = player_id
        self.chatbot = chatbot
        self.draw = BasicDraw()
        self.listener = listener

    def main_process(self):
        self.draw.ai_draw(True)
        self.draw.ai_draw(False)
        self.draw.player_draw(True)
        self.draw.player_draw(False)

        self.render_cards()

        bet_money = self.listener.ask_for_bet()
        if bet_money == 'giveup':
            self.chatbot.send_action_card(ActionCard(
                title="暗黑二十一点",
                text="### 你输了！呵呵...",
                btns=[CardItem(
                    title="再来一把", url="**游戏:暗黑二十一点:来一把")]
            ))
            return
        bet_money = int(bet_money)
        current_money = user_login.get_luck_point_by_sender_id(self.player_id)['value']
        if bet_money >= current_money:
            self.chatbot.send_text('你梭哈了，当前的所有金币：「{0}」全部用于下注！'.format(current_money))
            bet_money = current_money
        self.push_money(bet_money)

        while Ai.predict_point(self.draw.player_cards)['status'] == 'none':
            call_command = self.listener.ask_for_call()
            if call_command == 'call':
                self.draw.player_draw(False)
                self.render_cards()
            if call_command == 'done':
                break

        self.chatbot.send_text("轮到AI的回合...")
        eventlet.sleep(1)

        while Ai.predict_point(self.draw.ai_cards)['status'] == 'none':
            call_command = Ai.calculate_decision(self.draw)
            if call_command == 'call':
                self.chatbot.send_text("AI觉得应该再来一张...")
                eventlet.sleep(1)
                self.draw.ai_draw(False)
                self.render_cards()
            if call_command == 'done':
                self.chatbot.send_text("AI觉得牌够了")
                eventlet.sleep(1)
                break

        judgement = Ai.judge(self.draw)
        self.render_cards(True)
        if judgement > 0:
            self.chatbot.send_action_card(ActionCard(
                title="暗黑二十一点",
                text="### 你赢了！「{0}」金币都是你的！".format(bet_money * 2),
                btns=[CardItem(
                    title="再来一把", url="**游戏:暗黑二十一点:来一把")]
            ))
            user_login.rewards(bet_money * 2, self.player_id, self.chatbot, '玩家')
        elif judgement < 0:
            self.chatbot.send_action_card(ActionCard(
                title="暗黑二十一点",
                text="### 你输了！呵呵...",
                btns=[CardItem(
                    title="再来一把", url="**游戏:暗黑二十一点:来一把")]
            ))
        else:
            self.chatbot.send_action_card(ActionCard(
                title="暗黑二十一点",
                text="### 平局！「{0}」金币还给你...".format(bet_money),
                btns=[CardItem(
                    title="再来一把", url="**游戏:暗黑二十一点:来一把")]
            ))
            user_login.rewards(bet_money, self.player_id, self.chatbot, '玩家')

    def push_money(self, count):
        user_login.give_the_lucky_point_to(-count, self.player_id)

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
        text = " # AI的牌：\n {0}\n # 你的牌：\n {1}".format(ai_cards_str, player_cards_str)
        self.chatbot.send_markdown(title="暗黑二十一点", text=text)
        eventlet.sleep(1)
