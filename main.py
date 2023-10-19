from randomness.sim_stats import Simulation, PokerTest, StdMean
from randomness.shuffling_algorithms import shuffle_np_random, shuffle_fisher_yates, shuffle_bin_shuffle

if __name__ == "__main__":
    file_name = "test_bin_shuffle-1.bin"
    # sim = Simulation()
    # sim.run(shuffle_bin_shuffle)
    # sim.save()
    test = PokerTest(file_name)
    test.load_dataset_bin(file_name)
    test.run()
        
