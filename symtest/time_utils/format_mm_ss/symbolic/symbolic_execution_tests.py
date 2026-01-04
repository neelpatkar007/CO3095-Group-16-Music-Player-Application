import unittest
from music_player.time_utils import  format_mm_ss

class TestSymbolicExecution(unittest.TestCase):
    """
    Test suite derived from symbolic path conditions (PC_1, PC_2).
    Variable S1 represents the 'seconds' input.
    """

    def test_pc1_none(self):
        # Path Condition PC_1: S1 is None
        s1 = None
        result = format_mm_ss(s1)
        self.assertEqual(result, "??:??")

    def test_pc1_negative(self):
        # Path Condition PC_1: S1 < 0
        s1 = -1.0
        result = format_mm_ss(s1)
        self.assertEqual(result, "??:??")

    def test_pc2_standard(self):
        # Path Condition PC_2: S1 >= 0
        # Specifically, 125.5 seconds should result in 02:05
        s1 = 125.5
        result = format_mm_ss(s1)
        self.assertEqual(result, "02:05")

if __name__ == "__main__":
    unittest.main()
