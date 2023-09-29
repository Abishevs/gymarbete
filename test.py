from main import Simulation, Test
# from main import Deck
sim = Simulation()
sim.run('np_shuffle')
sim.save()
test1 = Test('np_shuffle-1.npy')
