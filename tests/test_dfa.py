import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import unittest
from automata.dfa import Dfa

class DfaCase(unittest.TestCase):
    d1 = Dfa({'1', '2', '3'}, {'a', 'b'}, {('1', 'a', '2'), ('2', 'b', '3')}, '1', {'3'})
    d2 = Dfa({'1', '2', '3'}, {'a', 'b'}, {('1', 'a', '1'), ('1', 'b', '2'), ('2', 'a', '3'),\
                                           ('3', 'b', '1')}, '1', {'3'})
    d3 = Dfa({'1', '2', '3'}, {'a', 'b'}, {('1', 'a', '2'), ('2', 'b', '3')}, '1', {'1', '2'})

    def test_is_dfa_d1(self):
        self.assertTrue(self.d1.is_dfa(), True)

    def test_is_dfa_d2(self):
        self.assertTrue(self.d2.is_dfa(), True)

    def test_delta_function_1_a(self):
        self.assertEqual(self.d1.delta_function('1', 'a'), '2')

    def test_delta_function_1_b(self):
        self.assertEqual(self.d1.delta_function('1', 'b'), 's')

    def test_is_accepted_ab(self):
        self.assertTrue(self.d1.is_accepted('ab'))

    def test_is_accepted_aa(self):
        self.assertFalse(self.d1.is_accepted('aa'))

    def test_complement_d1(self):
        self.assertSetEqual(self.d1.complement().states, self.d3.states)
        self.assertSetEqual(self.d1.complement().alphabet, self.d3.alphabet)
        self.assertSetEqual(self.d1.complement().delta, self.d3.delta)
        self.assertEqual(self.d1.complement().start, self.d3.start)
        self.assertSetEqual(self.d1.complement().final, self.d3.final)

    def test_intersection_d1_d2(self):
        self.assertSetEqual(self.d1.intersection(self.d2).states, {'11', '21', 's3', 'ss', '32', 's1', 's2'})
        self.assertSetEqual(self.d1.intersection(self.d2).alphabet, {'a', 'b'})
        self.assertSetEqual(self.d1.intersection(self.d2).delta,

                            {('11', 'a', '21'), ('11', 'b', 's2'), ('21', 'a', 's1'), ('21', 'b', '32'),
                             ('s3', 'a', 'ss'), ('s3', 'b', 's1'), ('32', 'a', 's3'), ('32', 'b', 'ss'),
                             ('ss', 'a', 'ss'), ('ss', 'b', 'ss'), ('s1', 'a', 's1'), ('s1', 'b', 's2'),
                             ('s2', 'a', 's3'), ('s2', 'b', 'ss')})
        self.assertEqual(self.d1.intersection(self.d2).start, '11')
        self.assertSetEqual(self.d1.intersection(self.d2).final, set([]))

    def test_union_d1_d2(self):

        self.assertSetEqual(self.d1.union(self.d2).states, {'11', '21', 's3', 'ss', '32', 's1', 's2'})
        self.assertSetEqual(self.d1.union(self.d2).alphabet, {'a', 'b'})
        self.assertSetEqual(self.d1.union(self.d2).delta,
                            {('11', 'a', '21'), ('11', 'b', 's2'), ('21', 'a', 's1'), ('21', 'b', '32'),
                             ('s3', 'a', 'ss'), ('s3', 'b', 's1'), ('32', 'a', 's3'), ('32', 'b', 'ss'),
                             ('ss', 'a', 'ss'), ('ss', 'b', 'ss'), ('s1', 'a', 's1'), ('s1', 'b', 's2'),
                             ('s2', 'a', 's3'), ('s2', 'b', 'ss')})
        self.assertEqual(self.d1.union(self.d2).start, '11')
        self.assertSetEqual(self.d1.union(self.d2).final, {'s3', '32'})

    def test_set_difference_d1_d2(self):
        self.assertSetEqual(self.d1.set_difference(self.d2).states, {'11', '21', 's3', 'ss', '32', 's1', 's2'})
        self.assertSetEqual(self.d1.set_difference(self.d2).alphabet, {'a', 'b'})
        self.assertSetEqual(self.d1.set_difference(self.d2).delta,
                            {('11', 'a', '21'), ('11', 'b', 's2'), ('21', 'a', 's1'), ('21', 'b', '32'),
                             ('s3', 'a', 'ss'), ('s3', 'b', 's1'), ('32', 'a', 's3'), ('32', 'b', 'ss'),
                             ('ss', 'a', 'ss'), ('ss', 'b', 'ss'), ('s1', 'a', 's1'), ('s1', 'b', 's2'),
                             ('s2', 'a', 's3'), ('s2', 'b', 'ss')})
        self.assertEqual(self.d1.set_difference(self.d2).start, '11')
        self.assertSetEqual(self.d1.set_difference(self.d2).final, {'32'})

    def test_sym_difference_d1_d2(self):
        self.assertSetEqual(self.d1.sym_difference(self.d2).states, {'11', '21', 's3', 'ss', '32', 's1', 's2'})
        self.assertSetEqual(self.d1.sym_difference(self.d2).alphabet, {'a', 'b'})
        self.assertSetEqual(self.d1.sym_difference(self.d2).delta,
                            {('11', 'a', '21'), ('11', 'b', 's2'), ('21', 'a', 's1'), ('21', 'b', '32'),
                             ('s3', 'a', 'ss'), ('s3', 'b', 's1'), ('32', 'a', 's3'), ('32', 'b', 'ss'),
                             ('ss', 'a', 'ss'), ('ss', 'b', 'ss'), ('s1', 'a', 's1'), ('s1', 'b', 's2'),
                             ('s2', 'a', 's3'), ('s2', 'b', 'ss')})
        self.assertEqual(self.d1.sym_difference(self.d2).start, '11')
        self.assertSetEqual(self.d1.sym_difference(self.d2).final, {'32', 's3'})

    def test_is_universal_d1(self):
        self.assertFalse(self.d1.is_universal())

    def test_is_empty_d1(self):
        self.assertFalse(self.d1.is_empty())

    def test_is_included_d1_d2(self):
        pass

    def test_is_equal_d1_d2(self):
        pass

    def test_minimize_by_hopcroft_d1(self):
        pass

    def test_minimize_by_moore_d1(self):
        pass

    def test_minimize_by_brzozowski_d1(self):
        pass

    def test_convert_to_regex_d1(self):
        pass

if __name__ == '__main__':
    unittest.main()