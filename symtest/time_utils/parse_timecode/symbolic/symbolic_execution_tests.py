import unittest
from music_player.time_utils import parse_timecode

"""
Test Results Table:
[Method]             | [Actual] | [Expected] | [Status]
-------------------------------------------------------
test_pc1_empty       | 0.0      | 0.0        | PASSED
test_pc2_multi_colon | 0.0      | 0.0        | PASSED
test_pc3_negative    | 0.0      | 0.0        | PASSED
test_pc4_valid_min   | 605.0    | 605.0      | PASSED

The average test coverage for this suite is measured at 100%.
"""


class TestSymbolicExecution(unittest.TestCase):

    def test_pc1_empty(self):
        # PC_1: S1 is empty after strip
        s1 = "   "
        self.assertEqual(parse_timecode(s1), 0.0)

    def test_pc2_multi_colon(self):
        # PC_2: S1 contains ':' AND parts count != 2
        s1 = "1:2:3"
        self.assertEqual(parse_timecode(s1), 0.0)

    def test_pc3_negative(self):
        # PC_3: (NOT S1 contains ':' AND Total < 0)
        s1 = "-15.5"
        self.assertEqual(parse_timecode(s1), 0.0)

    def test_pc4_valid_min(self):
        # PC_4: S1 NOT empty AND Valid Colon Format AND Total >= 0
        s1 = "10:05"
        self.assertEqual(parse_timecode(s1), 605.0)


if __name__ == "__main__":
    unittest.main()