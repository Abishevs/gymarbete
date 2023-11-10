from randomness.utils import (evaluate_hand, 
                   shuffling_algo_wrapper,
                   get_shuffle_runs, 
                   get_shuffle_name, 
                   get_path,
                   gen_columns)
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import chisquare
import os

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


class BaseTest:
    """
    A base class for performing various statistical tests on shuffled decks.

    This class provides common functionalities and shared values like loading 
    dataset, clearing dataset, saving table and maintaining results in a 
    structured format. It's designed to be subclassed by specific statistical
    test implementions like Poker test or StdMean.

    Attributes:
    dataset (numpy.ndarray): loaded dataset for the tests.
    dataset_file_name (str): dataset file name for extracting name and iterations
    table (pandas.DataFrame): Table to store test results from all tests 

    Methods:
    load_dataset(file_path:str): given path to dataset loads it, should be an 1d array stored in .bin 
    save_table(file_name:str): Saves the result to a csv file
    run(): Abstract method, to be implemented by subclasses
    save(): Abstract method, save grahps/tables, to be implemnted by subclasses for specific tests
    
    """
    dataset = np.array([])
    dataset_file_name = ""
    table = pd.DataFrame(columns=gen_columns())

    def __init__(self,row_index=None, folder_name = "Result") -> None:
        # test can only take an specific file extension, change it to more generic way.
        self.dataset_file_name = BaseTest.dataset_file_name
        self.file_name = self.dataset_file_name.removesuffix(".bin")
        self.shuffle_name = get_shuffle_name(self.file_name)
        self.shuffle_runs =  get_shuffle_runs(self.file_name)
        self.result_file_name = f"{os.path.join(folder_name, self.file_name)}"
        self.table = BaseTest.table
        self.row_index = row_index
        
        # add general values to the table
        self.add_value("Algoritm", self.shuffle_name)
        self.add_value("Iteration", self.shuffle_runs)

    @classmethod
    def create_new_row(cls):
        new_row_index = len(cls.table)
        cls.table.loc[new_row_index] = [np.nan] * len(cls.table.columns)  # Initialize with NaNs
        return new_row_index

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
        """
        Loads a dataset given path, should follow an specific file format.
        and contain an flatten 2D array. 

        Example:
        riffle_shuffle-3.bin 

        Arguments:
            file_path (string): Path to dataset
        
        Raises: 
        FileLoadingError: If it can't find file, or it's in wrong format

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

    @classmethod
    def save_table(cls, result:str="table"):
        cls.table.to_csv(f"{result}.csv", index=False)

    def run(self):
        pass
        
    def save(self):
        pass

     
class PokerTest(BaseTest):
    """Takes 2darray as an argument
    Does calculations for the poker test.
    Occurencies of poker hands drawn from either the first 5 cards or proper poker way(2hand cards and 3 flop cards)
    Saves the image of the plotted result. where x=pokerhand type name and y=Occurencies
    """
    def __init__(self, row_index) -> None:
        super().__init__(row_index)
    
    def run(self):
        five_card_decks = self.shuffled_decks[:,[0,2,5,6,7]] # two player poker game, p1 two cards + flop
        result = np.apply_along_axis(evaluate_hand, axis=1, arr=five_card_decks) # returns 1d array containing hand_types

        # Create an array filled with zeros to represent the default counts for all hand types
        f_obs = np.zeros(10, dtype=int) # init observed

        hand_types, observed = np.unique(result, return_counts=True)

        # Fill in the observed counts into the init array
        f_obs[hand_types] = observed

        # expected frequencies
        f_exp = np.array([1628176,1372800,154440,68639,12751,6383,4681,780,45,5])

        CRITICAL_VALUE = 16.918977604620448 # with p-value 0.05 and df= 9
        P_VALUE = 0.05
        chi2_stat ,p_val = chisquare(f_obs=f_obs, f_exp=f_exp)
        self.add_value("X^2", chi2_stat)
        self.add_value("PVärde", p_val)
        self.add_value("Gräns värde", CRITICAL_VALUE)

        if p_val <= P_VALUE:
            # reject null hypothes, indicator of bias / non-randomness
            self.add_value("Signifikant", "Ja")
        else:
            # failed to reject null hypothes, it's random
           self.add_value("Signifikant", "Nej")

class StdMean(BaseTest):
    """
    1) Calculates mean position of each card in the deck
    2) Calcualtes how much each card deviates from mean position.
    Expected mean: 26 [52/2] 
    Expected std: as long as possible :D
    """
    def __init__(self, row_index) -> None:
        super().__init__(row_index)

    def run(self):
        # call it before each run. to clear prev memory.
        plt.figure()

        mean_pos = np.mean(self.shuffled_decks, axis=0)
        std_pos = np.std(self.shuffled_decks, axis=0)
        for i in range(52):
            # add values to tabel
            self.add_value(f"Kort{i}_Medelvärde", mean_pos[i])
            self.add_value(f"Kort{i}_Std", std_pos[i])
        
        plt.errorbar(range(52), mean_pos, yerr=std_pos,fmt='o')
        plt.xlabel('Korts position')
        plt.ylabel('Positons medelvärde')
        plt.title(f"Algortim: {self.shuffle_name}\niterationer: {self.shuffle_runs}\nDatamängds längd: {len(self.shuffled_decks)}")
        plt.savefig(self.result_file_name, facecolor='w', bbox_inches="tight",
                    pad_inches=0.3, transparent=True)

        plt.close()


if __name__ == "__main__":
    pass
