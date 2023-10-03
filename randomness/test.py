from utils import (evaluate_hand, 
                   get_shuffle_runs, 
                   get_shuffle_name, 
                   get_path)
from shuffling_algorithms import shuffle_np_random 
import matplotlib.pyplot as plt
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
    3.10:
        1) Implement PokerTest with hand type evaluation applied along axis=1 DONE
        2) Plot graph in PokerTest DONE
        3) Theoretical probalities of hand types appearing DONE, but hard coded!!!
"""

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
        self.deck = np.arange(52, dtype='int8')
        self.raw_data = np.tile(self.deck,(self.num_runs,1))  # int8 can store -+127, Do upcasting if numbers could exceed

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
        self.raw_data = np.apply_along_axis(shuffle_np_random, axis=1, arr=self.raw_data)


class BaseTest:
    """An base class of tests, mby if it has merit
    """
    def __init__(self, raw_data_file_name:str, folder_name = "Grahs&stuff") -> None:
        self.raw_data_file_name = raw_data_file_name.removesuffix(".npy")
        self.shuffle_name = get_shuffle_name(raw_data_file_name)
        self.shuffle_runs =  get_shuffle_runs(raw_data_file_name)
        self.result_file_name = f"{get_path(folder_name)}/{self.raw_data_file_name}"
        self._shuffled_decks = np.load(raw_data_file_name)

    @property
    def shuffled_decks(self):
        return self._shuffled_decks

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
        five_card_decks = self.shuffled_decks[:,[0,2,5,6,7]] # two player poker game, p1 two cards + flop
        result = np.apply_along_axis(evaluate_hand, axis=1, arr=five_card_decks) # returns 1d array containing hand_types
        hand_types, occurencies = np.unique(result, return_counts=True)

        # print(occurencies)
        # print(hand_types)
        # Create an array filled with zeros to represent the default counts for all hand types
        observed_counts = np.zeros(10, dtype=int)

        # Fill in the observed counts into the default array
        observed_counts[hand_types] = occurencies

        # Normalize the counts to probabilities
        total_counts = np.sum(observed_counts)
        observed_probabilities = observed_counts / total_counts

        # theoretical probabilities. Copy pasted from internet xd 
        theoretical_probabilities = np.array([0.501177, 0.422569, 0.047539, 0.021128, 0.003925, 0.001965, 0.001441, 0.0002401, 0.000139, 0.0000154])

        # x-axis labels
        label_dict = {0: "High Card", 1: "Pair", 2: "Two Pair", 3: "Three of a Kind", 4: "Straight", 5: "Flush", 6: "Full House", 7: "Four of a Kind", 8: "Straight Flush", 9: "Royal Flush"}

        # Plotting
        plt.figure(figsize=(10, 6))
        plt.plot(range(10), theoretical_probabilities, 'r-', label='Theoretical Probability')
        plt.plot(range(10), observed_probabilities, 'bo-', label='Observed Probability')
        
        # customasition
        plt.xlabel('Hand Type')
        plt.ylabel('Probability')
        plt.yscale('log')
        plt.title('Comparison of Theoretical and Observed Poker Hand Probabilities')
        plt.xticks(range(10), [label_dict[i] for i in range(10)], rotation=-90)
        plt.legend()
        plt.grid(True)

        plt.savefig(self.result_file_name, facecolor='y', bbox_inches="tight",
                     pad_inches=0.3, transparent=True)
        # plt.show()

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
    test.run("shuffle_np_random")
    test.save()
