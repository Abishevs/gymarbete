from randomness.sim_stats import Simulation, PokerTest
from randomness.shuffling_algorithms import shuffle_np_random

if __name__ == "__main__":
    sim = Simulation(num_runs=3250000)
    sim.run(shuffle_np_random)
    sim.save()
    test = PokerTest("np_random-1.npy")
    test.run()
        
