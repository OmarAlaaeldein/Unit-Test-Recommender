import unittest
from numerical_letter_grade import numerical_letter_grade

class TestNumericLetterGrade(unittest.TestCase):
    def test_numeric_letter_grade(self):
        # Test with sample data
        self.assertEqual(numerical_letter_grade([4.0, 3, 1.7, 2, 3.5]), ['A+', 'B', 'C-', 'C', 'A-'])

        # Test with edge cases
        self.assertEqual(numerical_letter_grade([1.2]), ['D+'])
        self.assertEqual(numerical_letter_grade([0.0]), ['E'])
        self.assertEqual(numerical_letter_grade([-1.0]), ['E'])

if __name__ == '__main__':
    unittest.main()