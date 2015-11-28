import unittest
from dfa import Dfa

class DfaCase(unittest.TestCase):
    def test_delta_function(self):
        d = Dfa({'1', '2', '3'}, {'a', 'b'}, {('1', 'a', '2'), ('2', 'b', '3')}, '1', {'3'})
        self.assertEqual(d.delta_function('1', 'a'), '2')

if __name__ == '__main__':
    unittest.main()