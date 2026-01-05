import unittest
from music_player.time_utils import  format_mm_ss

class TestSymbolicExecution(unittest.TestCase):

    def test_pc1_none(self):
        s1 = None
        result = format_mm_ss(s1)
        self.assertEqual(result, "??:??")

    def test_pc1_negative(self):
        s1 = -1.0
        result = format_mm_ss(s1)
        self.assertEqual(result, "??:??")

    def test_pc2_standard(self):
        s1 = 125.5
        result = format_mm_ss(s1)
        self.assertEqual(result, "02:05")

if __name__ == "__main__":
    unittest.main()
