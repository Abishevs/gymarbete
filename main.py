from poker_calc.deck.deck import Deck as Dk
from poker_calc.utils.ranker import evaluate_hand
from phevaluator.card import Card
import numpy as np

class Deck:
    def __init__(self) -> None:
        self.cards = np.array([card for card in range(52)])
"""
TODO: 
    1) Write diffrent shuffling algorithms enhiriting the base class 
        1.1) Algorithm: Fisher-yates (as base test)
        1.2) Riffle-shuffle
        1.3) 
    2) Pogram that can save sequences as raw data to be then analysed 
    includes:
        2.1) 2d np.array[[0 <= x <= 51],[...]...] 
        2.2) filenameas has following: algorithm_name-num.npy where num is how many shuffles were done by iteration
    3) Build a system that can do our predifined tests and save those charts/digrams and other usefull info.
        3.1) Frequncie analys / pattern matching
        3.2) Poker test
        3.3) ApEn
    4) Analys of charts and diagrams (self done after)
"""
RUNS = 6000 # how many times will it shuffle
ALGORITHM = "np_random_shuffle"
num_shuffles = 1

# Contains an binary 2d np.array where each row is list of [0 <= x <= 51]
raw_data_file = f"{ALGORITHM}-{num_shuffles}.npy" # algorith-1 means that that it shuffled 1 time

# Creates an 2d empty raw data set
# 1mil rows=52mb
raw_data = np.zeros((RUNS, 52), dtype='int8')  # int8 can store -+127, Do upcasting if numbers could exceed

for i in range(RUNS):
    deck = Deck()
    for runs in range(num_shuffles):
        np.random.shuffle(deck.cards)

    # adds array to pre existing 2d empty array
    raw_data[i, :] = deck.cards

np.save(raw_data_file, raw_data)

# load back in the dataset
loaded_array = np.load(raw_data_file) 

card5 =  Card(int(loaded_array[0, 4])) # turn num repr to card object, if nedeed
card =  Card(int(loaded_array[RUNS-1, 0])) # last row if RUNS var avialble 
card2 =  Card(int(loaded_array[len(loaded_array)-1, 1])) # takes the lenght aka size of dataset
card3 =  Card(int(loaded_array[0, 2])) # Takes 3 card from the first row, np.array syntax
card4 =  Card(int(loaded_array[0][3])) # Less efficient python list syntax of taking the 4 card from first row
print(card, card2,card3,card4,card5)
print(loaded_array[0, 0]) # repr as np.int8 (not python int, be cerefull).has it own repr and str method
