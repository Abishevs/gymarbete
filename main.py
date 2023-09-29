from random import shuffle
from poker_calc.deck.deck import Deck as Dk
from poker_calc.utils.ranker import evaluate_hand
from phevaluator.card import Card
from collections import Counter
import matplotlib.pyplot as plt
import os
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
    def __init__(self, raw_data_file_name:str, folder_name = "Grahs&stuff") -> None:
        file_name = raw_data_file_name.removesuffix(".npy").split('-')
        self.raw_data_file_name = raw_data_file_name.removesuffix(".npy")
        self.shuffle_name = file_name[0].capitalize().replace("_", " ") 
        self.shuffle_runs = file_name[1]
        self.folder_path = self.folder_name(folder_name)
        self.result_file_name = f"{self.folder_path}/{self.raw_data_file_name}"
        self._shuffled_decks = np.load(raw_data_file_name)

    @property
    def shuffled_decks(self):
        return self._shuffled_decks
    
    def folder_name(self,folder_name):
        current_dir = os.getcwd()
        path = os.path.join(current_dir, folder_name)
        if not os.path.exists(path):
            os.mkdir(path)
        return path


     
class PokerTest(Test):
    """Takes 2darray as an argument
    Does calculations for the poker test.
    Occurencies of poker hands drawn from either the first 5 cards or proper poker way(2hand cards and 3 flop cards)
    Saves the image of the plotted result. where x=pokerhand type name and y=Occurencies
    """
    def __init__(self, shuffled_decks_file) -> None:
        super().__init__(shuffled_decks_file)
    
    def draw_hand(self,column):
        """Returns an np.array with size 5"""
        return self.shuffled_decks[column, :5]

    def run(self):
        for i in range(len(self.shuffled_decks)):
            print(self.draw_hand(i))

class StdMean(Test):
    """Does pattern matching shaningans
    """
    def __init__(self, shuffled_decks_file) -> None:
        super().__init__(shuffled_decks_file)

    def run(self):

        mean_pos = np.mean(self.shuffled_decks, axis=0)
        std_pos = np.std(self.shuffled_decks, axis=0)
        
        plt.errorbar(range(52), mean_pos, yerr=std_pos,fmt='o')
        plt.xlabel('Card index')
        plt.ylabel('Mean position')
        plt.title(f"Shuffle name:{self.shuffle_name}; iterations: {self.shuffle_runs}\nDataset lenght: {len(self.shuffled_decks)} rows")
        plt.savefig(self.result_file_name, facecolor='y', bbox_inches="tight",
                    pad_inches=0.3, transparent=True)

def evaluate_hand(hand: list[Card]) -> int:
    """ Assuming that hand list is sorted by the highest rank as the last elemenet
    returns relative hand strenght value from 0-9
    """
    MAX = 5
    if len(hand) == MAX:
        # High card - low card == 4 # if True its a straight
        ranks = [card.get_rank for card in hand]
        dict_ranks = Counter(ranks)
        common_ranks = sorted(list(dict_ranks.values()))

        one_pair = common_ranks[-1] == 2 and common_ranks[-2] == 1
        two_pair = common_ranks[-1] == 2 and common_ranks[-2] == 2
        trips =  max(common_ranks) == 3 and common_ranks[-2] == 1 # aka theere of a kind
        straight = hand[-1].value - hand[0].value == 4 
        wheel = hand[-1].value == 14 and hand[-2].value == 5 # when Ace is the low card straight to 5
        flush = len(set(card.suite for card in hand)) == 1 
        fullhouse =  max(common_ranks) == 3 and common_ranks[-2] == 2
        quads =  max(common_ranks) == 4 # aka four of a kind
        royal_flush =  straight and flush and hand[0].value == 10

        if one_pair: 
            return 1 
        elif two_pair: 
            return 2
        elif trips: 
            return 3
        elif not flush and straight or wheel:
            return 4
        elif not straight and flush:
            return 5
        elif fullhouse:
            return 6
        elif quads:
            return 7
        elif wheel or straight and flush: # Straight flush 
            return 8 
        elif royal_flush:
            return 9
        return 0
    else:
        raise ValueError("Gotta be excatly 5 cards")

# RUNS = 6000 # how many times will it shuffle
ALGORITHM = "np_random_shuffle"
num_shuffles = 1
#
# # Contains an binary 2d np.array where each row is list of [0 <= x <= 51]
raw_data_file = f"{ALGORITHM}-{num_shuffles}.npy" # algorith-1 means that that it shuffled 1 time
#
# # Creates an 2d empty raw data set
# # 1mil rows=52mb
# raw_data = np.zeros((RUNS, 52), dtype='int8')  # int8 can store -+127, Do upcasting if numbers could exceed
#
# for i in range(RUNS):
#     deck = Deck()
#     for runs in range(num_shuffles):
#         np.random.shuffle(deck.cards)
#
#     # adds array to pre existing 2d empty array
#     raw_data[i, :] = deck.cards
#
# np.save(raw_data_file, raw_data)
#
# # load back in the dataset
# loaded_array = np.load(raw_data_file) 
#
# card5 =  Card(int(loaded_array[0, 4])) # turn num repr to card object, if nedeed
# card =  Card(int(loaded_array[RUNS-1, 0])) # last row if RUNS var avialble 
# card2 =  Card(int(loaded_array[len(loaded_array)-1, 1])) # takes the lenght aka size of dataset
# card3 =  Card(int(loaded_array[0, 2])) # Takes 3 card from the first row, np.array syntax
# card4 =  Card(int(loaded_array[0][3])) # Less efficient python list syntax of taking the 4 card from first row
# print(card, card2,card3,card4,card5)
# print(loaded_array[0, 0]) # r pfepr as np.int8 (not python int, be cerefull).has it own repr and str method
test1 = StdMean(raw_data_file)
test1.run()
