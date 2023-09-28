from random import shuffle
from poker_calc.deck.deck import Deck as Dk
from poker_calc.utils.ranker import evaluate_hand
from phevaluator.card import Card
import numpy as np

"""
TODO: Overview
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
"""
TODO:
    29.09:
        1) Make an reusable program for running shuffles and saving them
        2) Start building reusable test suite program, to do pattern matching, poker Test and or ApEn
            2.1) Look into how to save pictures automaticly with matplotlib, without actualy ploting it.
            2.2) If that works, all of the tests can be done within one program run.
        3) ... 

"""

class Deck:
    def __init__(self) -> None:
        self.cards = np.array([card for card in range(52)])

    def np_shuffle(self):
        np.random.shuffle(self.cards) 

    def fisher_yates(self):
        pass
        # print("FIsher Yates")

    def riffle_shuffle(self):
        pass

class Simulation:
    """Defines simulation parameters.
    In a loop does shuffles and swaps them to pre genereated zerod 2d np.array.
    Saves the simulation data as an .npy file with with filename that gives context of which shuffle it is
    and how many times it shuffled the deck.


    """
    def __init__(self) -> None:
        self.num_runs : int = 10
        self.num_shuffles : int = 1 
        self.shuffle_name = ""
        self.raw_data = np.zeros((self.num_runs, 52), dtype='int8')  # int8 can store -+127, Do upcasting if numbers could exceed

    def save(self):
        """Saves the 2d np.array to external file
        """
        raw_data_file = f"{self.shuffle_name}-{self.num_shuffles}.npy" # algorith-1 means that that it shuffled 1 time
        np.save(raw_data_file, self.raw_data)

    def run(self, shuffling_algorithm_name:str):
        """
        Runs the simulation using predifined parameters
        """
        self.shuffle_name = shuffling_algorithm_name
        for i in range(self.num_runs):
            deck = Deck() #  
            shuffle = getattr(deck, shuffling_algorithm_name) # gets the method of the shuffling algorithm
            for _ in range(self.num_shuffles):
                shuffle() # runs deck.chosen_algorithm

            # swaps shuffled array with an pre existing 2d zeroed array container
            self.raw_data[i, :] = deck.cards

class Test:
    """An base class of tests, mby if it has merit
    """
    def __init__(self, raw_data_file_name:str) -> None:
        self.two_d_array = np.load(raw_data_file_name)

class PokerTest(Test):
    """Takes 2darray as an argument
    Does calculations for the poker test.
    Occurencies of poker hands drawn from either the first 5 cards or proper poker way(2hand cards and 3 flop cards)
    Saves the image of the plotted result. where x=pokerhand type name and y=Occurencies
    """
    def __init__(self) -> None:
        super().__init__()

    def run(self):
        pass

class PatternMatching(Test):
    """Does pattern matching shaningans
    """
    def __init__(self) -> None:
        super().__init__()

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
print(loaded_array[0, 0]) # r pfepr as np.int8 (not python int, be cerefull).has it own repr and str method
