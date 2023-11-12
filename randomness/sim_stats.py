from enum import Enum
import math
import re
from typing import Union
from randomness.utils import (evaluate_hand, 
                   shuffling_algo_wrapper,
                   get_shuffle_runs, 
                   get_shuffle_name, 
                   get_path,
                   )
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import chisquare
import os

# DATASET_LENGHT = 3248700
DATASET_LENGHT = 3250000
ROW_LENGHT = 52
DTYPE = np.int8

class FileLoadingError(Exception):
    pass

class DatasetShapeError(Exception):
    pass

class InvalidFrequencyError(Exception):
    pass

class InvalidFileNameFormatError(Exception):
    pass

class Column(Enum):
    """
    columns in Pandas data frame for the tests
    """

    ALGORITHM =  "Algoritm"
    ITERATIONS =  "Iterationer"
    CHI2_STAT = "X^2"
    P_VALUE = "PVärde"
    CRITICAL_VALUE = "Gräns värde"
    ISSIGNIFICANT = "Signifikant"

    # dynamic members
    @staticmethod
    def card_mean(i):
        if 0 <= i <= 51:
            return f"Kort{i}_Medelvärde"
        else:
            raise KeyError(f"key: {i} is out of bound")

    @staticmethod
    def card_std(i):
        if 0 <= i <= 51:
            return f"Kort{i}_Std"
        else:
            raise KeyError(f"key: {i} is out of bound")

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
    columns = [col.value for col in Column]
    dynamic_columns = [Column.card_std(i) for i in range(52)] + [Column.card_mean(i) for i in range(52)]
    return columns + dynamic_columns

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
        __init__(row_index:int, folder_name:str= "Result"): pass in row index and optional folder for result graphs
        create_new_row(cls): class  method to Initialize an new row and get index of that row
        load_dataset(file_path:str): given path to dataset loads it, should be an 1d array stored in .bin 
        save_table(file_name:str): Saves the result to a csv file
        run(): Abstract method, to be implemented by subclasses
        save(): Abstract method, save grahps/tables, to be implemnted by subclasses for specific tests
    
    """
    dataset = np.array([])
    dataset_file_name = ""
    table = pd.DataFrame(columns=gen_columns())

    def __init__(self,row_index=None, folder_name = "Result") -> None:
        """
        Arguments:
            row_index(BaseTest.create_new_row()): create a shared row for subclassed tests
            folder_name(str): grahps result folder name
        """

        self.file_name = BaseTest.dataset_file_name
        self.shuffle_name = get_shuffle_name(self.file_name)
        self.shuffle_runs =  get_shuffle_runs(self.file_name)
        self.result_folder = folder_name
        self.result_file_name = f"{os.path.join(self.result_folder, self.file_name)}"
        self.table = BaseTest.table
        self.row_index = row_index
        
        # add general values to the table
        self.add_value(Column.ALGORITHM, self.shuffle_name)
        self.add_value(Column.ITERATIONS, self.shuffle_runs)


    @classmethod
    def create_new_row(cls):
        """
        Initializes an NaN value row to be populated by each test

        Returns:
            Initialized row index to be used for other tests, to populate the same row
        """
        new_row_index = len(cls.table)
        cls.table.loc[new_row_index] = [np.nan] * len(cls.table.columns)  # Initialize with NaNs
        return new_row_index

    def add_value(self, column: Union[Column, str] , value):
        """
        Add a value to pandas dataframe

        Arguments:
            column (Column | str): column in dataframe
            value (str): value to add

        Example 1:
            self.add_value(Column.CHI2_STAT, 134.234)

        Example 2:
            self.add_value(Column.card_mean(card_index), 123.234)

        """
        column_name = column.value if isinstance(column, Column) else column
        self.table.loc[self.row_index, column_name] = value

    @property
    def shuffled_decks(self):
        return BaseTest.dataset
    
    @classmethod
    def validate_file_name(cls, file_name:str):
        """
        Checks if file follows: algo name seperated by underscore
        followed by a hypheen follow by an one or more digits indicating interations

        Arguments:
            file_name(str): file name without file extension

        Raises:
            InvalidFileNameFormatError: if file format is structured wrong 
        """

        pattern = re.compile(r'^[a-zA-Z0-9_]+-\d+$')
        if not pattern.match(file_name):
            raise InvalidFileNameFormatError(f"Invalid file name format: '{file_name}'. Expected format 'algo_name-iterationsnum'")


    @classmethod
    def load_dataset(cls, file_path:str):
        """
        Loads a dataset given path, should follow an specific file format.

        Example:
            riffle_shuffle-3.bin or riffle_shuffle-3.npy [should be an 2d array]

        Wrong example:
            riffleshuffle.bin [should include iterations as int]

        Arguments:
            file_path (string): Path to dataset
        
        Raises: 
            InvalidFileNameFormatError: if file format is structured wrong 
            FileLoadingError: If it can't find file, or it's in wrong format
            DatasetShapeError: if it can't reshape given array

        """
        file_name, file_extension = os.path.splitext(file_path)
        file_name = os.path.basename(file_name)

        try:
            # validate that file is an proper format, raise an error otherwise
            cls.validate_file_name(file_name)

            if file_extension == ".npy":
                cls.dataset = np.load(file_path)
                if cls.dataset.ndim != 2 or cls.dataset.shape[1] != ROW_LENGHT:
                    raise DatasetShapeError(f"Shape mismatch for .npy file: Expected 2D array with {ROW_LENGHT} columns, got {cls.dataset.shape}")

            else:
                flatten_dataset = np.fromfile(file_path, dtype=DTYPE)

                # check if flatten dataset is an multiple of rows
                if flatten_dataset.size % ROW_LENGHT != 0:
                    raise DatasetShapeError(f"Dataset size missmatch: Expected multiple of {ROW_LENGHT}, got {flatten_dataset.size}")

                # calculate number of rows
                dataset_lenght = flatten_dataset.size // ROW_LENGHT

                # reshape back into 2D array and set it as class global variable
                cls.dataset = flatten_dataset.reshape((dataset_lenght, ROW_LENGHT))
        
            # extract shuffle name + iterations from file name
            cls.dataset_file_name = os.path.basename(file_name)

            # check if its expected shape
            if cls.dataset.shape[1] != ROW_LENGHT:
                raise DatasetShapeError(f"Row lenght missmatch: Expected {ROW_LENGHT}, got {cls.dataset.shape[1]}")

        # if file was not found
        except OSError as e:
            raise FileLoadingError(f"File not found {file_path}") from e

    
    @classmethod
    def clear_dataset(cls):
        cls.dataset = np.array([])

    @classmethod
    def save_table(cls, result_folder:str = "Result", result_file_name:str="table"):
        result_file_name =f"{result_file_name}.csv" 
        result_file_name = f"{os.path.join(result_folder, result_file_name)}"
        cls.table.to_csv(result_file_name, index=False)

    def run(self):
        pass
        
    def save(self):
        pass

     
class PokerTest(BaseTest):
    """
    Performs pokertest given 2D array of card decks
    chooses 5 cards from each deck and evualutes it to
    an pokerhand. Calculates how many of each pokerhand
    type there is. Uses observed frequencies and expected
    (which are calculated before hand) to calculate chi-
    square statistic x^2 and p_value (probability value)
    add results to the pandas dataframe.

    """
    def __init__(self, row_index) -> None:
        super().__init__(row_index)
        
    
    def run(self):
        """
        Tailord specificly for Pokerhand types as bins for chi-square
        Thus min dataset lenght:  2598960*1.25 = 3248700 which gives =>
        5 statisticly expected royal flushes(4*1.25=5). As chi-square test is 
        invalid if smallest bin is smaller than 5 by it's defintion: 
        https://www.itl.nist.gov/div898/handbook/eda/section3/eda35f.htm

        Adds result from pokertest to pandas dataframe: Basetest.table

        Raises:
            InvalidFrequencyError: if expected frequency for royal flushes is less than 5

        """
        # expected frequencies 52 choose 5 = 2'598'960
        # thus each handtype is distributed:
        # min is default * 1.25 to get atleast 5 expected royal flushes
        default = math.comb(52, 5)
        if self.shuffled_decks.shape[0] < (default*1.25):
            raise InvalidFrequencyError(f"Dataset: {self.shuffled_decks.shape[0]} is too small to perform pokertest")

        f_exp = np.array([1302540,1098240,123552 ,54912,10200,5108, 3744, 624, 36, 4], dtype=np.float64)

        # get the factor from the dataset divded by the default for a single deck
        factor = self.shuffled_decks.shape[0] / default

        # update expected freqencies with the desired factor
        f_exp *= factor

        five_card_decks = self.shuffled_decks[:,[0,2,5,6,7]] # two player poker game, p1 two cards + flop
        result = np.apply_along_axis(evaluate_hand, axis=1, arr=five_card_decks) # returns 1d array containing hand_types

        # Create an array filled with zeros to represent the default counts for all hand types
        f_obs = np.zeros(10, dtype=int) # init observed

        hand_types, observed = np.unique(result, return_counts=True)

        # Fill in the observed counts into the init array
        f_obs[hand_types] = observed

        CRITICAL_VALUE = 16.918977604620448 # with p-value 0.05 and df= 9
        P_VALUE = 0.05
        chi2_stat ,p_val = chisquare(f_obs=f_obs, f_exp=f_exp)
        self.add_value(Column.CHI2_STAT, chi2_stat)
        self.add_value(Column.P_VALUE, p_val)
        self.add_value(Column.CRITICAL_VALUE, CRITICAL_VALUE)

        if p_val <= P_VALUE:
            # reject null hypothes, indicator of bias / non-randomness
            self.add_value(Column.ISSIGNIFICANT, "Ja")
        else:
            # failed to reject null hypothes, it's random
           self.add_value(Column.ISSIGNIFICANT, "Nej")

class StdMean(BaseTest):
    """
    1) Calculates mean position of each card in the deck
    2) Calcualtes how much each card deviates from mean position.
    Expected mean: 26 [52/2] 
    Expected std: 

    Saves result as image of the plot in result directory
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
            self.add_value(Column.card_mean(i), mean_pos[i])
            self.add_value(Column.card_std(i), std_pos[i])
        
        plt.errorbar(range(52), mean_pos, yerr=std_pos,fmt='o')
        plt.xlabel('Korts position')
        plt.ylabel('Positons medelvärde')
        plt.title(f"Algortim: {self.shuffle_name}\niterationer: {self.shuffle_runs}\nDatamängds längd: {len(self.shuffled_decks)}")
        plt.savefig(self.result_file_name, facecolor='w', bbox_inches="tight",
                    pad_inches=0.3, transparent=True)

        plt.close()


if __name__ == "__main__":
    pass
