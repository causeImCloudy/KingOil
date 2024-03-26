import logging
from random import shuffle
from src.Card import *
    

class Deck:
    def __init__(self):
        self.Cards = []
        self.DeckIndex = -1
        
        production_card_distribution = {
            '1-1': {
                500: {'total': 0, 'with_property': 0},
                1000: {'total': 1, 'with_property': 1},
                2000: {'total': 1, 'with_property': 1},
                3000: {'total': 1, 'with_property': 0},
                4000: {'total': 1, 'with_property': 0},
            },
            '1-2': {
                500: {'total': 5, 'with_property': 2},
                1000: {'total': 1, 'with_property': 1},
                2000: {'total': 1, 'with_property': 0},
                3000: {'total': 1, 'with_property': 0},
                4000: {'total': 1, 'with_property': 0},
            },
            '1-3': {
                500: {'total': 1, 'with_property': 0},
                1000: {'total': 1, 'with_property': 1},
                2000: {'total': 2, 'with_property': 0},
                3000: {'total': 1, 'with_property': 0},
                4000: {'total': 1, 'with_property': 0},
            },
            '1-4': {
                500: {'total': 2, 'with_property': 1},
                1000: {'total': 0, 'with_property': 0},
                2000: {'total': 2, 'with_property': 0},
                3000: {'total': 1, 'with_property': 0},
                4000: {'total': 1, 'with_property': 0},
            },
        }

        for x in range(5):
            self.AddCard(
                Card("OilDepletion", 0, 500, 1, False)
            )
        
        for x in range(2):
            self.AddCard(
                Card("FireDamage", -1, 0, 0, False)
            )

        for wells, earnings_info in production_card_distribution.items():
            for production, card_info in earnings_info.items():
                # Cards with property
                for _ in range(card_info['with_property']):
                    self.AddCard(Card(
                        name=f"{wells} Wells - ${production}",
                        production=production,
                        basePay=0,
                        wells=wells,
                        property=True
                    ))

                # Cards without property
                for _ in range(card_info['total'] - card_info['with_property']):
                    self.AddCard(Card(
                        name=f"{wells} Wells - ${production}",
                        production=production,
                        basePay=0,
                        wells=wells,
                        property=False
                    ))

        self._shuffle()

    def _shuffle(self):
        shuffle(self.Cards)
        self.DeckIndex = 0
    
    def DrawCard(self):
        """
            Checks if the deck needs to be shuffled then returns the card from the deck index
        """

        if self.DeckIndex >= len(self.Cards):
            self.DeckIndex = -1
            self._shuffle()

        returnCard = self.Cards[self.DeckIndex]
        self.DeckIndex += 1

        return returnCard

    def AddCard(self, card):
        self.Cards.append(card)
       
    def GetCards(self):
        return self.Cards


if __name__ == "__main__":
    
    deck = Deck()
    
    print(len(deck.GetCards()))
    for card in deck.GetCards():
        print(f"{card.GetName()} prop:{card.HasProperty()} production:{card.GetProduction()}")
        print(f"wells {card.GetWells()}")

    