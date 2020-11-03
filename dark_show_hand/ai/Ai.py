from dark_show_hand.ai.AnalysisFace import make_cards
from dark_show_hand.ai.PredictFace import predict_face
from dark_show_hand.desk.Draw import Draw


class Ai:
    def __init__(self, bet):
        self.bet = bet
        pass

    def think(self, draw, player_order=None):
        # bet_type: 下注类型
        # 'normal' 常规下注
        # 'ai_give_up' 玩家放弃
        # bet_count：下注金额
        bet_count = 10
        if player_order is not None:
            bet_count = self.bet.player_bet - self.bet.ai_bet
            self.bet.chatbot.send_text('AI跟注，下注金额：{0}'.format(bet_count))
        return {
            'bet_type': self.calculate_decision(draw),
            'bet_count': bet_count
        }

    def think_show_hand(self, draw, order):
        return self.think(draw, order)

    def calculate_decision(self, draw):
        # 先思考彼此是什么货色
        ai_predict_face_result = predict_face(draw.ai_cards)
        player_predict_face_result = predict_face(draw.player_cards[1:])
        # 不考虑终极变态牌面，因为概率极低
        if ai_predict_face_result['max_kind'] >= player_predict_face_result['max_kind']:
            return 'normal'
        else:
            if ai_predict_face_result['is_straight'] and player_predict_face_result['max_kind'] < 3:
                # if ai_predict_face_result['needed'] in player_predict_face_result['needed']:
                #     return 'giveup'
                # else:
                return 'normal'
            else:
                return 'ai_give_up'


if __name__ == "__main__":
    draw = Draw()
    ai = Ai(None)
    draw.ai_cards = make_cards(['♥️10', '♥️8', '♦️11', '♦️9'])
    draw.player_cards = make_cards(['♣️7', '♣️7', '♥️7', '♦️6'])
    print(ai.calculate_decision(draw))
