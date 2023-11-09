from randomness.utils import (evaluate_hand, 
                   shuffling_algo_wrapper,
                   get_shuffle_runs, 
                   get_shuffle_name, 
                   get_path)
from randomness.shuffling_algorithms import shuffle_np_random 
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import chisquare
import os

"""
TODO: Overview
    1) Write log file and for each write an .csv file with: 
        1.1) Chi-square value
        1.2) p_value 
        1.3) For stdMean. write mean position and std for each card.
"""
"""
TODO:
    Week: 45.
    - [] Save value ploted in graphs, all of em
"""
DATASET_LENGHT = 3248700
ROW_LENGHT = 52
DTYPE = np.int8

class FileLoadingError(Exception):
    pass

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

def gen_columns():
    columns = []
    columns.append("Algoritm")
    columns.append("Iteration")
    columns.append("X^2")
    columns.append("PVärde")
    columns.append("Gräns värde")
    for i in range (52):
        columns.append(f"Kort{i}_Medelvärde")
        columns.append(f"Kort{i}_Std")
    return columns

class BaseTest:
    """An base class of tests, mby if it has merit
    """
    dataset = np.array([])
    dataset_file_name = ""
    table = pd.DataFrame(columns=gen_columns())

    def __init__(self, folder_name = "Result") -> None:
        # test can only take an specific file extension, change it to more generic way.
        self.dataset_file_name = BaseTest.dataset_file_name
        self.file_name = self.dataset_file_name.removesuffix(".bin")
        self.shuffle_name = get_shuffle_name(self.file_name)
        self.shuffle_runs =  get_shuffle_runs(self.file_name)
        self.result_file_name = f"{os.path.join(folder_name, self.file_name)}"
        self.table = BaseTest.table
        self.row_index = self.set_row()

    def set_row(self):
        return len(self.table)

    def add_value(self, column:str, value):
        self.table.loc[self.row_index, column] = value

    @property
    def shuffled_decks(self):
        return BaseTest.dataset
    
    @classmethod
    def load_dataset_np(cls, file_name:str):
        """Loads .npy file. which contains an 2D array
        
        Arguments:
            file_name (string): Path to dataset
        """
        try:
            cls.dataset =  np.load(file_name)
            cls.dataset_file_name = file_name
        except Exception as e:
            raise FileLoadingError(f"Failed to load file {file_name}") from e

    @classmethod
    def load_dataset(cls, file_path:str):
        """Loads dataset file. which contains an flatten 2d array
        
        Arguments:
            file_path (string): Path to dataset
        
        Raises: FileLoadingError  
        """

        try:
            flatten_dataset = np.fromfile(file_path, dtype=DTYPE)
            dataset = flatten_dataset.reshape((DATASET_LENGHT, ROW_LENGHT))
            cls.dataset = dataset 
            cls.dataset_file_name = os.path.basename(file_path) 
        except Exception as e:
            raise FileLoadingError(f"Failed to load file {file_path}") from e
    
    @classmethod
    def clear_dataset(cls):
        cls.dataset = np.array([])

    def run(self):
        pass
        
    def save(self):
        print(self.table)
        pass
     
class PokerTest(BaseTest):
    """Takes 2darray as an argument
    Does calculations for the poker test.
    Occurencies of poker hands drawn from either the first 5 cards or proper poker way(2hand cards and 3 flop cards)
    Saves the image of the plotted result. where x=pokerhand type name and y=Occurencies
    """
    def __init__(self) -> None:
        super().__init__()
    
    def run(self):
        # print(self.shuffled_decks)
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
        self.add_value("X^2", chi2_stat)
        # self.table["x^2"].append(p_val)
        # self.table["critical value"].append(chi2_stat)
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
    """
    1) Calculates mean position of each card in the deck
    2) Calcualtes how much each card deviates from mean position.
    Expected mean: 26 [52/2] 
    Expected std: as long as possible :D
    """
    def __init__(self) -> None:
        super().__init__()

    def run(self):
        # call it before each run. to clear prev memory.
        plt.figure()

        mean_pos = np.mean(self.shuffled_decks, axis=0)
        std_pos = np.std(self.shuffled_decks, axis=0)
        for i in range(52):
            self.add_value(f"Kort{i}_Medelvärde", mean_pos[i])
            self.add_value(f"Kort{i}_Std", std_pos[i])
        
        plt.errorbar(range(52), mean_pos, yerr=std_pos,fmt='o')
        plt.xlabel('Card index')
        plt.ylabel('Mean position')
        plt.title(f"Shuffle name:{self.shuffle_name}\n iterations: {self.shuffle_runs}\nDataset lenght: {len(self.shuffled_decks)} rows")
        plt.savefig(self.result_file_name, facecolor='y', bbox_inches="tight",
                    pad_inches=0.3, transparent=True)
        # 
        plt.close()


if __name__ == "__main__":

    ALGORITHM = "np_random_shuffle"
    num_shuffles = 1
    raw_data_file = f"{ALGORITHM}-{num_shuffles}.npy" # algorith-1 means that that it shuffled 1 time
    # test = PokerTest("shuffle_np_random-1.npy")
    # test.run()
    test = Simulation()
    test.run(shuffle_np_random)
    test.save()
