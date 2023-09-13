from poker_calc.deck.deck import Deck
from poker_calc.utils.ranker import evaluate_hand
import csv

output_filename = "poker_hand_data.csv"

with open(output_filename, mode="w", newline="") as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(["Card 1", "Card 2", "Card 3", "Card 4", "Card 5", "Hand Type"])

    for i in range(100000):
        deck = Deck()  # Deck instance created
        deck.riffle_shuffel()
        deck.riffle_shuffel()
        drawn_cards = deck.cards[:5]
        res = evaluate_hand(drawn_cards)  # 5 cards drawn from the deck
        hand_type = res  # Get string representation of the hand type

        card_names = [str(card) for card in drawn_cards]
        csvwriter.writerow(card_names + [hand_type])

print(f"Poker hand data saved in '{output_filename}'.")
