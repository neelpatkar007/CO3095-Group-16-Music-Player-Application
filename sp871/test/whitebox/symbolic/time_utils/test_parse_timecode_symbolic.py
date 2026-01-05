import unittest
from music_player.time_utils import parse_timecode



class TestSymbolicExecution(unittest.TestCase):

    def test_pc1_empty(self):
        s1 = "   "
        self.assertEqual(parse_timecode(s1), 0.0)

    def test_pc2_multi_colon(self):
        s1 = "1:2:3"
        self.assertEqual(parse_timecode(s1), 0.0)

    def test_pc3_negative(self):
        s1 = "-15.5"
        self.assertEqual(parse_timecode(s1), 0.0)

    def test_pc4_valid_min(self):
        s1 = "10:05"
        self.assertEqual(parse_timecode(s1), 605.0)


if __name__ == "__main__":
    unittest.main()