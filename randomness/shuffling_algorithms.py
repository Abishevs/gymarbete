import numpy as np
import numba

def shuffle_np_random(deck:np.ndarray):
    np.random.shuffle(deck)
    return deck

@numba.jit('int8[:](int8[:])',nopython=True)
def shuffle_fisher_yates(deck:np.ndarray):
    n = len(deck)
    for i in range(n):
        j = np.random.randint(i, n)
        deck[i], deck[j] = deck[j], deck[i]

    return deck

def shuffle_bin_shuffle(deck):
    bins = [[] for _ in range(6)]  # Create 6 bins

    # Distribute cards into bins
    for card in deck:
        random_bin = np.random.randint(0, 5)
        bins[random_bin].append(card)

    # Reassemble the deck from bins
    deck_position = 0
    for bin in bins:
        for card in bin:
            deck[deck_position] = card
            deck_position += 1

    return deck

