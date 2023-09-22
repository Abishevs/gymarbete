import pickle
import ast
from poker_calc.deck.deck import Deck as Dk
from poker_calc.utils.ranker import evaluate_hand
import pandas as pd
import h5py
import numpy as np
# import csv

class Deck(Dk):
    def __init__(self) -> None:
        super().__init__()
    
    def shuffle(self):
        pass
"""
TODO: 
    1) Write diffrent shuffling algorithms enhiriting the base class 
        1.1) Algorithm 1
    2) Pogram that can save sequences as raw data to be then analysed 
    includes:
        2.1) Hur många gånger shuffled det(1,2,3..)
        2.2) Lista av alla kort
    3) Build a system that can do our predifined tests and save those charts/digrams and other usefull info.
        3.1) Frequncie analys 
        3.2) Poker test
        3.3) ApEn
    4) Analys of charts and diagrams (self done after)
"""
output_filename = "poker_hand_data1.csv"


# with open(output_filename, mode="w", newline="") as csvfile:
#     csvwriter = csv.writer(csvfile)
#     csvwriter.writerow(["Card 1", "Card 2", "Card 3", "Card 4", "Card 5", "Hand Type"])
def safe_eval(cell):
    return [str(item) for item in ast.literal_eval(cell)]

for i in range(100):
    deck = Deck()  # Deck instance created
    # deck.riffle_shuffel()
    # deck.riffle_shuffel()
    df = pd.DataFrame({
        'num_runs': [2],
        'deck': [deck.cards]
        })
    # if i == 1:
    #     df.to_csv(output_filename, mode='w', index=False)
    # df.to_csv(output_filename, mode='a', index=False)
print(f"Poker hand data saved in '{output_filename}'.")

dff = pd.read_csv(output_filename)
dff['deck'] = dff['deck'].apply(safe_eval)
print(dff['deck'][0])
# print(dff['cards'].apply(pickle.loads))
