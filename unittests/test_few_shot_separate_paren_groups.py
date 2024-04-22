import unittest
from separate_paren_groups import separate_paren_groups

class TestSeparateParenGroups(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(separate_paren_groups('( ) (( )) (( )( ))'), ['()', '(())', '(()())'])

    def test_nested(self):
        self.assertEqual(separate_paren_groups('(()()) ((())) () ((())()())'), [
            '(()())', '((()))', '()', '((())()())'
        ])

    def test_multiple_groups(self):
        self.assertEqual(separate_paren_groups('() (()) ((())) (((())))'), [
            '()', '(())', '((()))', '(((())))'
        ])


    def test_ignore_spaces(self):
        self.assertEqual(separate_paren_groups('   (   )   '), ['()'])

if __name__ == '__main__':
    unittest.main()