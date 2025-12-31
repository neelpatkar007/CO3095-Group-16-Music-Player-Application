import unittest
from music_player import time_utils


class TestTimeUtils(unittest.TestCase):
    """
    Black-Box Specification-based Testing for time_utils.py.
    Testing Tool: Python unittest
    Test Technique: Category Partition Method
    """

    # format_mm_ss Tests

    def test_format_valid_integers(self):
        """
        Expected Result: Returns "mm:ss" formatted string corresponding to input seconds.
        Actual Result: PASSED[100%]. Handled 0, 65, and 3600 seconds correctly.
        """
        # 0 seconds 00:00
        self.assertEqual(time_utils.format_mm_ss(0), "00:00")
        # 65 seconds 01:05
        self.assertEqual(time_utils.format_mm_ss(65), "01:05")
        # 3600 seconds 60:00
        self.assertEqual(time_utils.format_mm_ss(3600), "60:00")

    def test_format_valid_floats(self):
        """
        Expected Result: Float is cast to int and returns "mm:ss".
        Actual Result: Passed. 90.9 correctly formatted as 01:30.
        """
        # 90.9 seconds converted to 01:30
        self.assertEqual(time_utils.format_mm_ss(90.9), "01:30")

    def test_format_invalid_inputs(self):
        """
        Expected Result: Returns "??:??".
        Actual Result: Passed. Handled None and -5.0 correctly.
        """
        # None input
        self.assertEqual(time_utils.format_mm_ss(None), "??:??")
        # Negative input
        self.assertEqual(time_utils.format_mm_ss(-5.0), "??:??")

    # Parse Timecode Tests

    def test_parse_plain_seconds(self):
        """
        Expected Result: Returns float value of the string.
        Actual Result: Passed. "120" parsed as 120.0.
        """
        self.assertEqual(time_utils.parse_timecode("120"), 120.0)
        self.assertEqual(time_utils.parse_timecode("120.5"), 120.5)
        # Whitespace handling
        self.assertEqual(time_utils.parse_timecode("  60  "), 60.0)

    def test_parse_minutes_seconds(self):
        """
        Expected Result: Calculates total seconds as (minutes * 60) + seconds.
        Actual Result: Passed. Various "mm:ss" formats parsed correctly.
        """
        # 1:30 converted to 90.0
        self.assertEqual(time_utils.parse_timecode("1:30"), 90.0)
        # 0:45 converted to 45.0
        self.assertEqual(time_utils.parse_timecode("0:45"), 45.0)
        # 10:00 converted to 600.0
        self.assertEqual(time_utils.parse_timecode("10:00"), 600.0)
        # 2.5:30 converted to 180.0
        self.assertEqual(time_utils.parse_timecode("2.5:30"), 180.0)

    def test_parse_bytes_input(self):
        """
        Expected Result: Decodes bytes to string and parses correctly.
        Actual Result: Passed. b"60" correctly parsed as 60.0.
        """
        self.assertEqual(time_utils.parse_timecode(b"60"), 60.0)
        self.assertEqual(time_utils.parse_timecode(b"1:00"), 60.0)

    def test_parse_empty_input(self):
        """
        Expected Result: Returns 0.0 for empty input.
        Actual Result: Passed. Empty strings returned 0.0.
        """
        self.assertEqual(time_utils.parse_timecode(""), 0.0)
        self.assertEqual(time_utils.parse_timecode("   "), 0.0)
        self.assertEqual(time_utils.parse_timecode(b""), 0.0)

    def test_parse_negative_values(self):
        """
        Expected Result: Returns 0.0 for negative totals.
        Actual Result: Passed. "-10" and negative timecodes returned 0.0.
        """
        self.assertEqual(time_utils.parse_timecode("-10"), 0.0)
        self.assertEqual(time_utils.parse_timecode("-1:00"), 0.0)

    def test_parse_invalid_formats(self):
        """
        Expected Result: Returns 0.0 due to ValueError/TypeError handling.
        Actual Result: Passed. Invalid formats ("1:2:3", "abc") returned 0.0 safely.
        """
        # Too many colons
        self.assertEqual(time_utils.parse_timecode("1:2:3"), 0.0)
        # Non-numeric text
        self.assertEqual(time_utils.parse_timecode("abc"), 0.0)
        self.assertEqual(time_utils.parse_timecode("one:thirty"), 0.0)
        # Partial garbage
        self.assertEqual(time_utils.parse_timecode("120s"), 0.0)