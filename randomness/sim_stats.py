from randomness.utils import (evaluate_hand, 
                   shuffling_algo_wrapper,
                   get_shuffle_runs, 
                   get_shuffle_name, 
                   get_path)
from randomness.shuffling_algorithms import shuffle_np_random 
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import chisquare

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
    4.10:
        1) Think of possible values from poker test that might be used in analys/ result delen. 
        2) Rethink what u want to plot in the graph
        3) Implement chi-squared test in pokerTest
"""
DATASET_LENGHT = 3248700
ROW_LENGHT = 52
DTYPE = np.int8

class Simulation:
    """Defines simulation parameters.
    In a loop does shuffles and swaps them to pre genereated zerod 2d np.array.
    Saves the simulation data as an .npy file with with filename that gives context of which shuffle it is
    and how many times it shuffled the deck.
    """
    def __init__(self, num_runs = DATASET_LENGHT, num_shuffles = 1) -> None:
        self.num_runs : int = num_runs
        self.num_shuffles : int = num_shuffles 
        self.shuffle_name = ""
        self.deck = np.arange(ROW_LENGHT, dtype=DTYPE)
        self.raw_data = np.tile(self.deck,(self.num_runs,1))  # int8 can store -+127, Do upcasting if numbers could exceed

    def save(self):
        """Saves the 2d np.array to external file
        """
        raw_data_file = f"{self.shuffle_name}-{self.num_shuffles}.npy" # algorith-1 means that that it shuffled 1 time
        np.save(raw_data_file, self.raw_data)

    def run(self, shuffling_algorithm):
        """
        Runs the simulation using predifined parameters
        """
        self.shuffle_name = shuffling_algorithm.__name__.removeprefix("shuffle_")
        self.raw_data = np.apply_along_axis(shuffling_algo_wrapper, axis=1, arr=self.raw_data, algo=shuffling_algorithm )
        print(self.raw_data)


class BaseTest:
    """An base class of tests, mby if it has merit
    """
    def __init__(self, raw_data_file_name:str, folder_name = "Grahs&stuff") -> None:
        # test can only take an specific file extension, change it to more generic way.
        self.raw_data_file_name = raw_data_file_name.removesuffix(".bin")
        self.shuffle_name = get_shuffle_name(raw_data_file_name)
        self.shuffle_runs =  get_shuffle_runs(raw_data_file_name)
        self.result_file_name = f"{get_path(folder_name)}/{self.raw_data_file_name}"
        # self._shuffled_decks = np.load(raw_data_file_name)
        self.dataset = np.array([])

    @property
    def shuffled_decks(self):
        return self.dataset
    
    def load_dataset_np(self, file_name:str):
        self.dataset =  np.load(file_name)
    
    def load_dataset_bin(self, file_name:str):
        # binary file  is an flaten array
        flatten_dataset = np.fromfile(file_name, dtype=DTYPE)
        dataset = flatten_dataset.reshape((DATASET_LENGHT, ROW_LENGHT))
        self.dataset = dataset 

    def run(self):
        pass
     
class PokerTest(BaseTest):
    """Takes 2darray as an argument
    Does calculations for the poker test.
    Occurencies of poker hands drawn from either the first 5 cards or proper poker way(2hand cards and 3 flop cards)
    Saves the image of the plotted result. where x=pokerhand type name and y=Occurencies
    """
    def __init__(self, shuffled_decks_file) -> None:
        super().__init__(shuffled_decks_file)
    
    def run(self):
        print(self.shuffled_decks)
        five_card_decks = self.shuffled_decks[:,[0,2,5,6,7]] # two player poker game, p1 two cards + flop
        result = np.apply_along_axis(evaluate_hand, axis=1, arr=five_card_decks) # returns 1d array containing hand_types
        # Create an array filled with zeros to represent the default counts for all hand types

        f_obs = np.zeros(10, dtype=int)

        hand_types, observed = np.unique(result, return_counts=True)
        # Fill in the observed counts into the default array
        f_obs[hand_types] = observed
        print(hand_types)
        print(f_obs)
        # Observed occurencies vs expected. i could of course hard code those expected
        f_exp = np.array([1628176,1372800,154440,68639,12751,6383,4681,780,45,5])
        print(f'Sum of observed frequencies: {np.sum(f_obs)}')
        print(f'Sum of expected frequencies: {np.sum(f_exp)}')
        chi2_stat ,p_val = chisquare(f_obs=f_obs, f_exp=f_exp)
        print(chi2_stat)
        print(p_val)


        

        # Normalize the counts to probabilities
        # total_counts = np.sum(observed_counts)
        # observed_probabilities = observed_counts / total_counts

        # theoretical probabilities. Copy pasted from internet xd 
        # theoretical_probabilities = np.array([0.501177, 0.422569, 0.047539, 0.021128, 0.003925, 0.001965, 0.001441, 0.0002401, 0.000139, 0.0000154])

        # x-axis labels
        # label_dict = {0: "High Card", 1: "Pair", 2: "Two Pair", 3: "Three of a Kind", 4: "Straight", 5: "Flush", 6: "Full House", 7: "Four of a Kind", 8: "Straight Flush", 9: "Royal Flush"}
        #
        # # Plotting
        # plt.figure(figsize=(10, 6))
        # plt.plot(range(10), theoretical_probabilities, 'r-', label='Theoretical Probability')
        # plt.plot(range(10), observed_probabilities, 'bo-', label='Observed Probability')
        #
        # # customasition
        # plt.xlabel('Hand Type')
        # plt.ylabel('Probability')
        # plt.yscale('log')
        # plt.title('Comparison of Theoretical and Observed Poker Hand Probabilities')
        # plt.xticks(range(10), [label_dict[i] for i in range(10)], rotation=-90)
        # plt.legend()
        # plt.grid(True)
        #
        # plt.savefig(self.result_file_name, facecolor='y', bbox_inches="tight",
        #              pad_inches=0.3, transparent=True)
        # # plt.show()

class StdMean(BaseTest):
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


if __name__ == "__main__":

    ALGORITHM = "np_random_shuffle"
    num_shuffles = 1
    raw_data_file = f"{ALGORITHM}-{num_shuffles}.npy" # algorith-1 means that that it shuffled 1 time
    # test = PokerTest("shuffle_np_random-1.npy")
    # test.run()
    test = Simulation()
    test.run(shuffle_np_random)
    test.save()
