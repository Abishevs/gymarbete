import unittest
from  randomness import shuffling_algorithms as shuffle_module 
import numpy as np

class TestInPlaceShuffle(unittest.TestCase):

    def test_in_place_shuffle(self):
        for name, obj in vars(shuffle_module).items():
            if callable(obj) and 'shuffle_' in name:  # shuffle_ is the naming convetion of shuffle algoriths
                with self.subTest(msg=f"Testing {name}"):
                    original_array = np.arange(10)
                    original_id = id(original_array)

                    obj(original_array)  # Call the shuffle function

                    new_id = id(original_array)

                    self.assertEqual(original_id, new_id, f"Failed for {name}")

if __name__ == '__main__':
    unittest.main()
