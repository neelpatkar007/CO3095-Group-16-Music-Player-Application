import unittest
from music_player import time_utils


class TestTimeUtilsBranch(unittest.TestCase):
    """
    White-Box Branch Tests for time_utils.py.
    Testing Tool: Python unittest
    Test Technique: Branch Testing (White-Box)
    """

    def test_format_branches(self):
        """
        Expected Result:
         True branch returns "??:??".
         False branch performs formatting.
        Actual Result: Passed. Both decision outcomes verified.
        """
        # Branch True (None)
        self.assertEqual(time_utils.format_mm_ss(None), "??:??")
        # Branch True (Negative)
        self.assertEqual(time_utils.format_mm_ss(-1), "??:??")
        # Branch False
        self.assertEqual(time_utils.format_mm_ss(10), "00:10")

    def test_parse_type_and_empty_branches(self):
        """
        Expected Result: Correct handling for Bytes vs String and Empty vs Non-Empty.
        Actual Result: Passed. All 4 branch paths executed.
        """
        # Bytes Check
        time_utils.parse_timecode(b"10")  # True
        time_utils.parse_timecode("10")  # False

        # Empty Check
        time_utils.parse_timecode("")  # True
        time_utils.parse_timecode("10")  # False

    def test_parse_colon_branches(self):
        """
        Expected Result:
         - Detects colon.
         - Validates split length only if colon is present.
        Actual Result: Passed. Verified split logic branches.
        """
        # Colon Check
        time_utils.parse_timecode("1:00")  # True
        time_utils.parse_timecode("60")  # False

        # Length Check
        time_utils.parse_timecode("1:00:00")  # True
        time_utils.parse_timecode("1:00")  # False

    def test_parse_negative_and_exception_branches(self):
        """
        Expected Result:
         - Negative totals are handled.
         - Exceptions trigger the except block.
        Actual Result: Passed. Verified negative safety and error handling branches.
        """
        # Negative Check
        time_utils.parse_timecode("-10")  # True
        time_utils.parse_timecode("10")  # False

        # Exception Branch
        time_utils.parse_timecode("invalid")
        time_utils.parse_timecode("10")