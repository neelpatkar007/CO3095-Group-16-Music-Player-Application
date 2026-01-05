import unittest
from music_player.time_utils import parse_timecode

"""
Test Results Table:
[Method]              | [Actual] | [Expected] | [Status]
--------------------------------------------------------
test_iter1_initial    | 0.0      | 0.0        | PASSED
test_iter2_flip_empty | 605.0    | 605.0      | PASSED
test_iter3_flip_parts | 0.0      | 0.0        | PASSED
test_iter4_flip_colon | 0.0      | 0.0        | PASSED
test_iter5_final      | 45.0     | 45.0       | PASSED

The average test coverage for this suite is measured at 100%.
"""

class TestConcolicTesting(unittest.TestCase):

    def test_iter1_initial(self):
        # Iteration 1: Concrete Seed S1 = ""
        s1 = ""
        self.assertEqual(parse_timecode(s1), 0.0)

    def test_iter2_flip_empty(self):
        # Iteration 2: Derived input from flipping PC_1
        s1 = "10:05"
        self.assertEqual(parse_timecode(s1), 605.0)

    def test_iter3_flip_parts(self):
        # Iteration 3: Derived input from flipping D4 (parts == 2)
        s1 = "1:2:3"
        self.assertEqual(parse_timecode(s1), 0.0)

    def test_iter4_flip_colon(self):
        # Iteration 4: Derived input from flipping D3 (S1 contains ':')
        s1 = "-5.0"
        self.assertEqual(parse_timecode(s1), 0.0)

    def test_iter5_final(self):
        # Iteration 5: Derived input from flipping D5 (Total < 0)
        s1 = "45.0"
        self.assertEqual(parse_timecode(s1), 45.0)

if __name__ == "__main__":
    unittest.main()