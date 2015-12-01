import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import unittest
from automata.nfa import Nfa

class NfaCase(unittest.TestCase):
    n1 = Nfa({'1', '2', '3'}, {'a', 'b'}, {('1', 'a', '1'), ('1', 'a', '2'), ('1', 'b', '1'),
                                          ('2', 'b', '3')}, '1', {'3'})
    n2 = Nfa({'1', '2', '3'}, {'a', 'b'}, {('1', 'a', '2'), ('2', 'a', '2'), ('2', 'b', '2'), ('2', 'b', '3'),
                                           ('3', 'a', '1')}, '1', {'3'})

    def test_is_nfa_n1(self):
        self.assertTrue(self.n1.is_nfa())

    def test_is_nfa_n2(self):
        self.assertTrue(self.n2.is_nfa())

    def test_delta_function_n1_3_a(self):
        self.assertSetEqual(self.n1.delta_function('3', 'a'), set([]))

    def test_delta_function_n2_2_b(self):
        self.assertSetEqual(self.n2.delta_function('2', 'b'), {'2', '3'})

    def test_is_accepted(self):
        pass

    def test_convert_to_dfa_n1(self):
        pass

    def test_complement_n1(self):
        pass

    def test_intersection_n1_n2(self):
        pass

    def test_union_n1_n2(self):
        pass

    def test_set_difference_n1_n2(self):
        pass

    def test_sym_difference_n1_n2(self):
        pass

    def test_is_empty_n1(self):
        pass

    def test_is_universal_n1(self):
        pass

    def test_is_included_n1_n2(self):
        pass

    def test_is_equal_n1_n2(self):
        pass

if __name__ == '__main__':
    unittest.main()