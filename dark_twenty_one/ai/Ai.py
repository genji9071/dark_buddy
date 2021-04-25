from dark_twenty_one.desk.BasicDraw import BasicDraw
from infra.poker.PokerCard import make_cards


def calculate_decision(draw: BasicDraw):
    # 'call' 要牌
    # 'done' 终止要牌
    ai_point = predict_point(draw.ai_cards)
    player_point = predict_point(draw.player_cards)
    if player_point['status'] == 'boom' or ai_point['status'] == 'boom':
        return 'done'
    elif ai_point['status'] == 'blackjack' or ai_point['status'] == 'five' or ai_point['status'] == '21':
        return 'done'
    else:
        if ai_point['num'] < 16 < player_point['num']:
            return 'call'
        else:
            return 'done'


def predict_point(cards) -> dict:
    sum = 0
    num_a = 0
    num_jqk = 0
    status = 'none'
    for card in cards:
        if card['card'].number == 14:
            num_a += 1
            sum += 1
        else:
            if card['card'].number in [10, 11, 12, 13]:
                num_jqk += 1
                sum += 10
            else:
                sum += card['card'].number
    if sum > 21:
        status = 'boom'
    elif num_a == 1 and num_jqk == 1 and len(cards) == 2:
        return {
            'status': 'blackjack',
            'num': 21
        }
    elif len(cards) >= 5 and sum <= 21:
        status = 'five'
    elif num_a > 0 and sum <= 11:
        sum += 10
    if sum == 21:
        status = '21'
    return {
        'status': status,
        'num': sum
    }


def get_status_rank(point) -> int:
    if point['status'] == 'five':
        return 3
    elif point['status'] == 'blackjack':
        return 2
    elif point['status'] == '21':
        return 1
    elif point['status'] == 'none':
        return 0
    elif point['status'] == 'boom':
        return -1


def judge(draw: BasicDraw) -> int:
    ai_point = predict_point(draw.ai_cards)
    player_point = predict_point(draw.player_cards)
    ai_status_rank = get_status_rank(ai_point)
    player_status_rank = get_status_rank(player_point)
    if ai_status_rank == player_status_rank == 0:
        return player_point['num'] - ai_point['num']
    else:
        return player_status_rank - ai_status_rank


if __name__ == "__main__":
    draw = BasicDraw()
    draw.ai_cards = make_cards(['♥️8', '♥️7'])
    draw.player_cards = make_cards(['♠️14', '♥️3', '♣️10'])
    print(predict_point(draw.player_cards))
