from randomness.sim_stats import BaseTest, PokerTest, StdMean
from randomness.utils import get_path
from multiprocessing import Pool
import os

def run_tests(file_name:str):
    try:
        BaseTest.load_dataset_bin(file_name)

        # define test classes
        tests = [PokerTest(), StdMean()]
        for test in tests:
            test.run()
            test.save()
        # reset dataset after tests
        BaseTest.clear_dataset()

    except Exception as e:
       print(f"Error: {e}")

if __name__ == "__main__":
    data_folder = get_path("raw_data")  
    # dataset_names = ["test_bin_shuffle-1.bin", "test_bin_shuffle1.bin", "test_bin_shuffle-1.bin"]
    dataset_names = [os.path.join(data_folder, file_name) for file_name in os.listdir(data_folder)]
    # print(dataset_names)

    with Pool(processes=4) as pool:
    # for dataset_name in dataset_names:
        # run_tests(dataset_name)
        pool.map(run_tests, dataset_names)
