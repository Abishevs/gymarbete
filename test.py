from poker_calc.deck.deck import Deck as Dk
from poker_calc.utils.ranker import evaluate_hand
from poker_calc.constants.combos import COMBOS 
from copy import deepcopy

class Deck(Dk):
    def __init__(self) -> None:
        super().__init__()
       
    # def riffle_shuffel(self):
    #     pass
         


deck_orginal = Deck()

for i in range(2):
    deck = deepcopy(deck_orginal) # Use deep copy to have the same original object rather than creating a new deck
    print(deck)
    # print(deck.show_all_cards())
    deck.riffle_shuffel()
    deck.show_all_cards()
    res =  evaluate_hand(deck.cards[:5])
    print(COMBOS.get(res))
    