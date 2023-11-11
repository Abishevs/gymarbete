from randomness.sim_stats import BaseTest, PokerTest, StdMean
from randomness.utils import get_path
import os

def run_tests(file_path:str):
    try:
        BaseTest.load_dataset(file_path)
        row_index = BaseTest.create_new_row()

        # define test classes
        tests = (PokerTest(row_index), StdMean(row_index))
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
    datasets = [os.path.join(data_folder, file_name) for file_name in os.listdir(data_folder)]
    # print(dataset_names)
    
    # for dataset_name in datasets:
    #     run_tests(dataset_name)

    run_tests(datasets[0])
    print(BaseTest.table)
    BaseTest.save_table()
