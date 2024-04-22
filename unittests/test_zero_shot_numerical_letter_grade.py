import unittest
from numerical_letter_grade import numerical_letter_grade

class NumericalLetterGradeTests(unittest.TestCase):
    def test_all_gpas(self):
        grades = [4.0, 3, 1.7, 2, 3.5]
        actual = numerical_letter_grade(grades)
        expected = ["A+", "B", "C-", "C", "A-"]
        self.assertListEqual(actual, expected)

    def test_one_student(self):
        grades = [3.2]
        actual = numerical_letter_grade(grades)
        expected = ["B+"]
        self.assertListEqual(actual, expected)

    def test_no_students(self):
        grades = []
        actual = numerical_letter_grade(grades)
        expected = []
        self.assertListEqual(actual, expected)
