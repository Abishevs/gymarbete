# from main import Simulation, Test
# from poker_calc.constants.combos import COMBOS
# import matplotlib.pyplot as plt
# import numpy as np
#
# # Your frequency data (just for demonstration)
# freq_data = np.random.randint(0, 100, 10)
#
# # Create the plot
# plt.bar(range(10), freq_data)
#
# # Set x-tick labels
# plt.xticks(range(10), [COMBOS[i] for i in range(10)], rotation=-90)
#
# # Add labels and title
# plt.xlabel('Hand Type')
# plt.ylabel('Frequency')
# plt.title('Poker Hand Frequencies')
#
# # Show the plot
# plt.show()
#ygb



import matplotlib.pyplot as plt
import numpy as np

# Your actual data. Let's say frequencies for now
actual_data = [1000, 2000, 3000, 4000, 5000, 4000, 3000, 2000, 1000, 500]

# Your theoretical probabilities. This is just an example.
theoretical_probabilities = [0.1, 0.15, 0.2, 0.25, 0.05, 0.1, 0.05, 0.05, 0.025, 0.025]

# Calculate expected frequencies
total_rounds = sum(actual_data)
expected_frequencies = [prob * total_rounds for prob in theoretical_probabilities]

# x-axis labels
label_dict = {0: "High Card", 1: "Pair", 2: "Two Pair", 3: "Three of a Kind", 4: "Straight", 5: "Flush", 6: "Full House", 7: "Four of a Kind", 8: "Straight Flush", 9: "Royal Flush"}

# Plotting
plt.bar(range(10), actual_data, alpha=0.6, label='Actual Data')
plt.plot(range(10), expected_frequencies, color='red', marker='o', linestyle='dashed', linewidth=2, markersize=6, label='Theoretical Frequencies')
plt.xticks(range(10), [label_dict[i] for i in range(10)], rotation=90)
plt.legend()
plt.show()

