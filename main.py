from randomness.sim_stats import Simulation, PokerTest
from randomness.shuffling_algorithms import shuffle_np_random, shuffle_fisher_yates, shuffle_bin_shuffle

if __name__ == "__main__":
    sim = Simulation(num_runs=3250000)
    sim.run(shuffle_bin_shuffle)
    sim.save()
    test = PokerTest("bin_shuffle-1.npy")
    test.run()
        
