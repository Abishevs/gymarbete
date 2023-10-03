import numpy as np 
import os

def get_path(folder_name):
        current_dir = os.getcwd()
        path = os.path.join(current_dir, folder_name)
        if not os.path.exists(path):
            os.mkdir(path)
        return path

def get_shuffle_name(file_name:str):
    base_name = file_name.removesuffix(".npy").split('-')
    return base_name[0].capitalize().replace('-', ' ')

def get_shuffle_runs(file_name:str):
    base_name = file_name.removesuffix(".npy").split('-')
    return base_name[-1]

def evaluate_hand(hand: np.ndarray) -> np.int8:
    """
    :type hand: np.ndarray[np.int8]
    """
    assert hand.shape == (5,)
    assert hand.dtype == 'int8'
        
    ranks = hand % 13 # ranks 0-12 aka card value
    ranks.sort()
    suites = hand // 13 # suites 0-3

    def is_flush():
        unique_suites = np.unique(suites)
        return len(unique_suites) == 1

    def is_straight():
        unique_ranks = np.unique(ranks)

        if len(unique_ranks) != 5:
            return False # imposible to have an straight, quit checking

        max_rank, min_rank = np.max(unique_ranks), np.min(unique_ranks)
        if max_rank - min_rank == 4:
            return True
        
        if max_rank == 12:
            # hard coded check for wheel :))
            if set(unique_ranks) == {0,1,2,3,12}:
                return True 

        return False

    def is_royal_flush():
        return is_straight() and is_flush() and np.min(ranks) == 8

    def rank_counts():
        _,counts = np.unique(ranks, return_counts=True)
        return counts

    counts = rank_counts()
    if is_royal_flush(): 
        return np.int8(9) # Royal flush

    elif is_flush() and is_straight(): 
        return np.int8(8) # straight flush

    elif 4 in counts: 
        return np.int8(7) # Quads 

    elif 3 in counts and 2 in counts:
        return np.int8(6) # Full house

    elif is_flush():
        return np.int8(5) # Flush

    elif is_straight():
        return np.int8(4) # Straight

    elif 3 in counts:
        return np.int8(3) # Trips

    elif np.count_nonzero(counts == 2) == 2: 
        return  np.int8(2) # Two pair

    elif 2 in counts:
        return np.int8(1) # Pair

    else:
        return np.int8(0) # no match= High cards 
