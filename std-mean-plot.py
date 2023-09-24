from random import randint
from poker_calc.deck.deck import Deck as Dk
from poker_calc.utils.ranker import evaluate_hand
from phevaluator.card import Card
import numpy as np
import matplotlib.pyplot as plt

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
RUNS = 1000000 # how many times will it shuffle
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
        np.random.seed(randint(0,15320))
        np.random.shuffle(deck.cards)

    # adds array to pre existing 2d empty array
    raw_data[i, :] = deck.cards

np.save(raw_data_file, raw_data)

# load back in the dataset
loaded_array = np.load(raw_data_file) 


mean_pos = np.mean(loaded_array, axis=0)
std_pos = np.std(loaded_array, axis=0)

plt.errorbar(range(52), mean_pos, yerr=std_pos,fmt='o')
plt.xlabel('Card')
plt.ylabel('Mean position')
plt.title("Mean and std  dev  of card  position over runs")
plt.show()
