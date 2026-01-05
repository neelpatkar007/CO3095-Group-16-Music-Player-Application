import unittest
from music_player.time_utils import  format_mm_ss

class TestConcolicTesting(unittest.TestCase):

    def test_iter1_initial(self):
        s1 = None
        self.assertEqual(format_mm_ss(s1), "??:??")

    def test_iter2_flipped(self):
        s1 = 125.5
        self.assertEqual(format_mm_ss(s1), "02:05")

    def test_iter3_flipped(self):
        s1 = -5.0
        self.assertEqual(format_mm_ss(s1), "??:??")

if __name__ == "__main__":
    unittest.main()
