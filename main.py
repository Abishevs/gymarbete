from randomness.sim_stats import BaseTest, PokerTest, StdMean
from randomness.utils import get_path
import os, logging

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
        logging.error(f"{e}")
       # print(f"Error: {e}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    data_folder = get_path("raw_data")  
    datasets = [os.path.join(data_folder, file_name) for file_name in os.listdir(data_folder)]
    
    for dataset_name in datasets:
        run_tests(dataset_name)

    # run_tests(datasets[0])
    print(BaseTest.table)
    BaseTest.save_table()
