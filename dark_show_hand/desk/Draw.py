from infra.poker.PokerCard import PokerCard
from lib.RandomLib import random


class Draw:
    def __init__(self):
        self.cards = []
        self.player_cards = []
        self.ai_cards = []

        for i in range(0, 4):
            type = PokerCard.TYPES[i]
            for j in range(2, 15):
                self.cards.append(PokerCard(type, j))
        random.seed()
        random.shuffle(self.cards)

    def draw(self, is_hidden: bool) -> (PokerCard, PokerCard):
        player_card = self.cards.pop()
        ai_card = self.cards.pop()
        self.player_cards.append({
            'is_hidden': is_hidden,
            'card': player_card
        })
        self.ai_cards.append({
            'is_hidden': is_hidden,
            'card': ai_card
        })
        return player_card, ai_card
