from dark_show_hand.ai.AnalysisFace import make_cards


def _is_straight(ranks):
    dis = (max(ranks) - min(ranks))
    needed = []
    max_rank = None
    might = dis <= 4 and len(set(ranks)) == len(ranks)
    if might:
        max_rank = max(ranks) + 4 - dis
        if max_rank > 14:
            max_rank = 14
        for i in range(1, len(ranks)):
            if max(ranks) - i not in ranks and max(ranks) - i >= 2:
                needed.append(max(ranks) - i)
        fill = 5 - len(ranks) - len(needed)
        for j in range(1, fill + 1):
            if max(ranks) + j <= 14:
                needed.append(max(ranks) + j)
            if min(ranks) - j >= 2:
                needed.append(min(ranks) - j)
    return might, max_rank, needed


def _is_flush(ranks):
    needed = []
    max_rank = None
    might = len(set(ranks)) <= 2
    if might:
        max_rank = _kind(ranks)[1]
        needed = list(set(ranks))
    return might, max_rank, needed


def _kind(ranks):
    for n in [4, 3, 2]:
        collect = []
        for s in ranks:
            if ranks.count(s) == n:
                collect.append(s)
        if collect:
            return n, max(collect)
    return 1, max(ranks)


def predict_face(target_cards: list) -> dict:
    target_cards = list(map(lambda x: x['card'], target_cards))
    target_cards = sorted(target_cards, key=lambda x: x.number)
    numbers = list(map(lambda x: x.number, target_cards))
    is_straight, straight_max_rank, straight_needed = _is_straight(numbers)
    is_flush, flush_max_rank, flush_needed = _is_flush(numbers)
    max_kind, kind_max_rank = _kind(numbers)

    max_rank = max(0 if not straight_max_rank else straight_max_rank, 0 if not flush_max_rank else flush_max_rank,
                   kind_max_rank)
    needed = set()
    needed.update(straight_needed)
    needed.update(flush_needed)

    return {
        'cards': target_cards,
        'is_flush': is_flush,
        'is_straight': is_straight,
        'max_kind': max_kind,
        'max_number': max_rank,
        'needed': list(needed)
    }


if __name__ == "__main__":
    print(predict_face(make_cards(['♣️13', '♥️13', '♠️9', '♠️9'])))
    # print(_is_straight([3, 4, 5, 7]))
