import unittest
from typing import List, Optional, Tuple
from find_closest_elements import find_closest_elements
import random

class TestFindClosestElements(unittest.TestCase):

    def test_single_element_list(self):
        self.assertEqual(find_closest_elements([1]), None)

    def test_two_element_list(self):
        self.assertEqual(find_closest_elements([1, 2]), (1, 2))

    def test_multiple_identical_elements(self):
        self.assertEqual(find_closest_elements([1, 2, 2, 3]), (2, 2))


if __name__ == "__main__":
    unittest.main()