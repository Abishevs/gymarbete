from randomness.sim_stats import Simulation, StdMean
import numpy as np

if __name__ == "__main__":
    # sim = Simulation()
    # sim.run(np.random.shuffle)
    # sim.save()
    test = StdMean("np_random_shuffle-1.npy")
    test.run()
        
