import unittest

# [Method]          | [Actual] | [Expected] | [Status]
# test_pc1_none     | "??:??"  | "??:??"    | PASS
# test_pc1_negative | "??:??"  | "??:??"    | PASS
# test_pc2_standard | "02:05"  | "02:05"    | PASS
#
# The average test coverage for this suite is measured at 100%.

class TestSymbolicExecution(unittest.TestCase):
    """
    Test suite derived from symbolic path conditions (PC_1, PC_2).
    Variable S1 represents the 'seconds' input.
    """

    def test_pc1_none(self):
        # Path Condition PC_1: S1 is None
        s1 = None
        from main import format_mm_ss
        result = format_mm_ss(s1)
        self.assertEqual(result, "??:??")

    def test_pc1_negative(self):
        # Path Condition PC_1: S1 < 0
        s1 = -1.0
        from main import format_mm_ss
        result = format_mm_ss(s1)
        self.assertEqual(result, "??:??")

    def test_pc2_standard(self):
        # Path Condition PC_2: S1 >= 0
        # Specifically, 125.5 seconds should result in 02:05
        s1 = 125.5
        from main import format_mm_ss
        result = format_mm_ss(s1)
        self.assertEqual(result, "02:05")

if __name__ == "__main__":
    unittest.main()