import unittest
from separate_paren_groups import separate_paren_groups

class TestSeparateParenGroups(unittest.TestCase):
    def test_empty_input(self):
        self.assertEqual(separate_paren_groups(""), [])

    def test_single_group(self):
        self.assertEqual(separate_paren_groups("(())"), ["(())"])

    def test_multiple_groups(self):
        self.assertEqual(separate_paren_groups("( ) (( )) (( )( ))"), ["()", "(())", "(()())"])

    def test_nested_groups(self):
        self.assertEqual(separate_paren_groups("((()))((())))"), ["((()))", "((()))"])


if __name__ == '__main__':
    unittest.main()