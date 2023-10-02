import unittest
import numpy as np
from analyser.main import evaluate_hand

class TestPokerHandEvaluation(unittest.TestCase):

    def test_royal_flush(self):
        self.assertEqual(evaluate_hand(np.array([9, 8, 10, 12,11], dtype=np.int8)), np.int8(9))

    def test_straight_flush(self):
        self.assertEqual(evaluate_hand(np.array([7, 8, 9, 10, 11], dtype=np.int8)), np.int8(8))

    def test_four_of_a_kind(self):
        self.assertEqual(evaluate_hand(np.array([0, 13, 26, 39, 3], dtype=np.int8)), np.int8(7))

    def test_full_house(self):
        self.assertEqual(evaluate_hand(np.array([0, 13, 2, 15, 28], dtype=np.int8)), np.int8(6))

    def test_flush(self):
        self.assertEqual(evaluate_hand(np.array([0, 1, 2, 3, 7], dtype=np.int8)), np.int8(5))

    def test_straight(self):
        self.assertEqual(evaluate_hand(np.array([0, 14, 2, 16, 30], dtype=np.int8)), np.int8(4))

    def test_three_of_a_kind(self):
        self.assertEqual(evaluate_hand(np.array([0, 13, 26, 5, 19], dtype=np.int8)), np.int8(3))

    def test_two_pair(self):
        self.assertEqual(evaluate_hand(np.array([0, 13, 1, 14, 4], dtype=np.int8)), np.int8(2))

    def test_one_pair(self):
        self.assertEqual(evaluate_hand(np.array([0, 13, 2, 3, 4], dtype=np.int8)), np.int8(1))

    def test_high_card(self):
        self.assertEqual(evaluate_hand(np.array([0, 15, 3, 18, 48], dtype=np.int8)), np.int8(0))

    def test_wheel_straight_flush(self):
        self.assertEqual(evaluate_hand(np.array([39,40,51,42,41], dtype=np.int8)), np.int8(8))

    def test_wheel_straight(self):
        self.assertEqual(evaluate_hand(np.array([0, 14, 28, 51, 42], dtype=np.int8)), np.int8(4))

if __name__ == '__main__':
    unittest.main()
