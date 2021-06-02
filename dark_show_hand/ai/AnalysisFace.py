from infra.poker.PokerCard import make_cards


def _is_straight(ranks):
    return (max(ranks) - min(ranks)) == 4 and len(set(ranks)) == 5, max(ranks)


def _is_flush(ranks):
    return len(set(ranks)) == 2, _kind(ranks)[1]


def _kind(ranks):
    for n in [4, 3, 2]:
        for s in ranks:
            if ranks.count(s) == n: return n, s
    return 1, max(ranks)


def _is_two_pairs(ranks):
    m, l = _kind(ranks)
    ranks.reverse()
    n, h = _kind(ranks)
    if m == n == 2 and l != h:
        return True, h
    else:
        return False, h


def analysis_face(cards: list) -> dict:
    cards = list(map(lambda x: x['card'], cards))
    cards = sorted(cards, key=lambda x: x.number)
    numbers = list(map(lambda x: x.number, cards))
    is_flush, max_number = _is_flush(numbers)
    if not is_flush:
        is_straight, max_number = _is_straight(numbers)
        if not is_straight:
            max_kind, max_number = _kind(numbers)
            if max_kind == 2:
                is_two_pair, max_number = _is_two_pairs(numbers)
            else:
                is_two_pair = False
        else:
            max_kind = 1
            is_two_pair = False
    else:
        is_straight = False
        max_kind = 3
        is_two_pair = False

    return {
        'cards': cards,
        'is_flush': is_flush,
        'is_straight': is_straight,
        'max_kind': max_kind,
        'is_two_pair': is_two_pair,
        'max_number': max_number
    }


def _royal_flush(player_cards, ai_cards):
    player_types = list(map(lambda x: x.type, player_cards['cards']))
    ai_types = list(map(lambda x: x.type, ai_cards['cards']))
    if len(set(player_types)) == 1 and player_cards['max_number'] == 15 and player_cards['is_straight']:
        return 0
    elif len(set(ai_types)) == 1 and ai_cards['max_number'] == 15 and ai_cards['is_straight']:
        return 1
    return None


def _straight_flush(player_cards, ai_cards):
    player_types = list(map(lambda x: x.type, player_cards['cards']))
    ai_types = list(map(lambda x: x.type, ai_cards['cards']))
    x = len(set(player_types)) == 1 and player_cards['is_straight']
    y = len(set(ai_types)) == 1 and ai_cards['is_straight']
    if x and not y:
        return 0
    elif y and not x:
        return 1
    elif x and y:
        return _high(player_cards, ai_cards)
    return None


def _four(player_cards, ai_cards):
    if player_cards['max_kind'] == 4 and ai_cards['max_kind'] < 4:
        return 0
    elif ai_cards['max_kind'] == 4 and player_cards['max_kind'] < 4:
        return 1
    elif player_cards['max_kind'] == 4 and ai_cards['max_kind'] == 4:
        return _high(player_cards, ai_cards)
    return None


def _three(player_cards, ai_cards):
    if player_cards['max_kind'] == 3 and ai_cards['max_kind'] < 3:
        return 0
    elif ai_cards['max_kind'] == 3 and player_cards['max_kind'] < 3:
        return 1
    elif player_cards['max_kind'] == 3 and ai_cards['max_kind'] == 3:
        return _high(player_cards, ai_cards)
    return None


def _two(player_cards, ai_cards):
    if player_cards['max_kind'] == 2 and ai_cards['max_kind'] < 2:
        return 0
    elif ai_cards['max_kind'] == 2 and player_cards['max_kind'] < 2:
        return 1
    elif player_cards['max_kind'] == 2 and ai_cards['max_kind'] == 2:
        return _high(player_cards, ai_cards)
    return None


def _two_pair(player_cards, ai_cards):
    if player_cards['is_two_pair'] and not ai_cards['is_two_pair']:
        return 0
    elif ai_cards['is_two_pair'] and not player_cards['is_two_pair']:
        return 1
    elif player_cards['is_two_pair'] and ai_cards['is_two_pair']:
        return _high(player_cards, ai_cards)
    return None


def _high(player_cards, ai_cards):
    return 0 if player_cards['max_number'] >= ai_cards['max_number'] else 1


def _flush(player_cards, ai_cards):
    if player_cards['is_flush'] and not ai_cards['is_flush']:
        return 0
    elif ai_cards['is_flush'] and not player_cards['is_flush']:
        return 1
    elif player_cards['is_flush'] and ai_cards['is_flush']:
        return _high(player_cards, ai_cards)
    return None


def _straight(player_cards, ai_cards):
    if player_cards['is_straight'] and not ai_cards['is_straight']:
        return 0
    elif ai_cards['is_straight'] and not player_cards['is_straight']:
        return 1
    elif player_cards['is_straight'] and ai_cards['is_straight']:
        return _high(player_cards, ai_cards)
    return None


def _solo_high(player_cards, ai_cards):
    for i in [4, 3, 2, 1, 0]:
        if player_cards['cards'][i].number > ai_cards['cards'][i].number:
            return 0
        if player_cards['cards'][i].number < ai_cards['cards'][i].number:
            return 1
    return 0


# _________________________________________________________________________________________________

def print_out(player_cards):
    cards = list(map(lambda x: x['card'], player_cards))
    cards_str = []
    for card in cards:
        cards_str.append(card.describe())
    return str(cards_str)


def judge(player_cards, ai_cards) -> int:
    player_cards = analysis_face(player_cards)
    ai_cards = analysis_face(ai_cards)
    result = _royal_flush(player_cards, ai_cards)
    if result is not None:
        return result
    result = _straight_flush(player_cards, ai_cards)
    if result is not None:
        return result
    result = _four(player_cards, ai_cards)
    if result is not None:
        return result
    result = _flush(player_cards, ai_cards)
    if result is not None:
        return result
    result = _straight(player_cards, ai_cards)
    if result is not None:
        return result
    result = _three(player_cards, ai_cards)
    if result is not None:
        return result
    result = _two_pair(player_cards, ai_cards)
    if result is not None:
        return result
    result = _two(player_cards, ai_cards)
    if result is not None:
        return result
    result = _solo_high(player_cards, ai_cards)
    if result is not None:
        return result


if __name__ == "__main__":
    player_cards = make_cards(['♦️8', '♥️9', '♣️7', '♥️6', '♠️5'])
    ai_cards = make_cards(['♣️10', '♦️9', '♠️8', '♠️2', '♥️3'])
    print(judge(player_cards, ai_cards))
