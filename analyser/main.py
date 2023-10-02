from random import shuffle
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
    2.10:
        1) Build evaluate hand function DONE
        2) Implement PokerTest with hand type evaluation applied along axis=1
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
    def __init__(self, num_runs = 1000000, num_shuffles = 1) -> None:
        self.num_runs : int = num_runs
        self.num_shuffles : int = num_shuffles 
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
        self.raw_data_file_name = raw_data_file_name.removesuffix(".npy")
        self.shuffle_name = sanitise_name(raw_data_file_name)
        self.shuffle_runs =  sanitise_name(raw_data_file_name, -1)
        self.result_file_name = f"{get_path(folder_name)}/{self.raw_data_file_name}"
        self._shuffled_decks = np.load(raw_data_file_name)

    @property
    def shuffled_decks(self):
        return self._shuffled_decks
    
def get_path(folder_name):
        current_dir = os.getcwd()
        path = os.path.join(current_dir, folder_name)
        if not os.path.exists(path):
            os.mkdir(path)
        return path

def sanitise_name(file_name:str, index:int = 0):
        """Splits string from shuffle_name-runs.npy 
        to shuffle name human readable and runs as char 
        """
        file_name_split = file_name.removesuffix(".npy").split('-')
        if index == 0:
            return file_name_split[index].capitalize().replace("_", " ")
        return file_name_split[-1]
     
class PokerTest(Test):
    """Takes 2darray as an argument
    Does calculations for the poker test.
    Occurencies of poker hands drawn from either the first 5 cards or proper poker way(2hand cards and 3 flop cards)
    Saves the image of the plotted result. where x=pokerhand type name and y=Occurencies
    """
    def __init__(self, shuffled_decks_file) -> None:
        super().__init__(shuffled_decks_file)
    
    def run(self):
        five_card_decks = self.shuffled_decks[:,[0,2,5,6,7]] # two player poker game, p1 two cards + flop
        result = np.apply_along_axis(evaluate_hand, axis=1, arr=five_card_decks) # returns 1d array containing hand_types
        hand_types, occurencies = np.unique(result, return_counts=True)
        # theoretical_occurencies = None # calculate theoritcal occurencies of each hand type to draw an red line idicating where idealy it should have landed.
        print(occurencies)
        print(hand_types)

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

def evaluate_hand(hand: np.ndarray) -> np.int8:
    """
    :type hand: np.ndarray[np.int8]
    """
    assert hand.shape == (5,)
    assert hand.dtype == 'int8'
        
    ranks = hand % 13 # ranks 0-12 aka card value
    ranks.sort()
    suites = hand // 13 # suites 0-3

    def is_flush():
        unique_suites = np.unique(suites)
        return len(unique_suites) == 1

    def is_straight():
        unique_ranks = np.unique(ranks)

        if len(unique_ranks) != 5:
            return False # imposible to have an straight, quit checking

        max_rank, min_rank = np.max(unique_ranks), np.min(unique_ranks)
        if max_rank - min_rank == 4:
            return True
        
        if max_rank == 12:
            # hard coded check for wheel :))
            if set(unique_ranks) == {0,1,2,3,12}:
                return True 

        return False

    def is_royal_flush():
        return is_straight() and is_flush() and np.min(ranks) == 8

    def rank_counts():
        _,counts = np.unique(ranks, return_counts=True)
        return counts

    counts = rank_counts()
    if is_royal_flush(): 
        return np.int8(9) # Royal flush

    elif is_flush() and is_straight(): 
        return np.int8(8) # straight flush

    elif 4 in counts: 
        return np.int8(7) # Quads 

    elif 3 in counts and 2 in counts:
        return np.int8(6) # Full house

    elif is_flush():
        return np.int8(5) # Flush

    elif is_straight():
        return np.int8(4) # Straight

    elif 3 in counts:
        return np.int8(3) # Trips

    elif np.count_nonzero(counts == 2) == 2: 
        return  np.int8(2) # Two pair

    elif 2 in counts:
        return np.int8(1) # Pair

    else:
        return np.int8(0) # no match= High cards 

if __name__ == "__main__":

    ALGORITHM = "np_random_shuffle"
    num_shuffles = 1
    raw_data_file = f"{ALGORITHM}-{num_shuffles}.npy" # algorith-1 means that that it shuffled 1 time
    test = PokerTest(raw_data_file)
    test.run()
