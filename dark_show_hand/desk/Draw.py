from config import random
from dark_show_hand.facade.Card import Card


class Draw:
    def __init__(self):
        self.cards = []
        self.player_cards = []
        self.ai_cards = []

        for i in range(0, 4):
            type = Card.TYPES[i]
            for j in range(2, 15):
                self.cards.append(Card(type, j))
        random.seed()
        random.shuffle(self.cards)

    def draw(self, is_hidden: bool) -> (Card, Card):
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
