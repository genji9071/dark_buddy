class PokerCard:
    __FANG_KUAI = '♦️'
    __HEI_TAO = '♠️'
    __CAO_HUA = '♣️'
    __HONG_TAO = '♥️'

    TYPES = [__CAO_HUA, __FANG_KUAI, __HONG_TAO, __HEI_TAO]

    def __init__(self, type, number):
        self.type = type
        self.number = number

    def __str__(self):
        return self.describe()

    def describe(self):
        number = self.number
        if number == 14:
            number = 'A'
        elif number == 11:
            number = 'J'
        elif number == 12:
            number = 'Q'
        elif number == 13:
            number = 'K'
        else:
            number = str(number)
        return '{0}{1}'.format(self.type, number)

    def bigger_than(self, card_b):
        return self.number > card_b.number


def make_cards(input):
    cards = []
    for per in input:
        cards.append({'card': PokerCard(per[0:1], int(per[2:]))})
    return cards
