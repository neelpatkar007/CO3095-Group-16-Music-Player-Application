import unittest
from music_player import time_utils


class TestTimeUtilsStatement(unittest.TestCase):
    """
    White-Box Statement Tests for time_utils.py.
    Testing Tool: Python unittest
    Test Technique: Statement Testing (White-Box)
    """

    def test_format_statements(self):
        """
        Expected Result:
         - Valid inputs execute math logic.
         - Invalid inputs execute early return.
        Actual Result: Passed.
        """
        # Early Return
        time_utils.format_mm_ss(None)

        # Calculation
        res = time_utils.format_mm_ss(65)
        self.assertEqual(res, "01:05")

    def test_parse_decoding_and_empty(self):
        """
        Expected Result: Bytes are decoded empty strings return 0.0.
        Actual Result: Passed.
        """
        # Bytes decoding
        self.assertEqual(time_utils.parse_timecode(b"60"), 60.0)

        # Empty string
        self.assertEqual(time_utils.parse_timecode("   "), 0.0)

    def test_parse_complex_logic(self):
        """
        Expected Result:
         - "MM:SS" enters split block.
         - Invalid format enters the exception block.
         - Negative result enters the negative check block.
        Actual Result: Passed. All logical blocks entered.
        """
        # MM:SS
        time_utils.parse_timecode("1:30")

        # Negative
        time_utils.parse_timecode("-10")

        # Exception Handler
        res = time_utils.parse_timecode("abc")
        self.assertEqual(res, 0.0)

    def test_parse_split_validation(self):
        """
        Expected Result: Input with multiple colons returns 0.0.
        Actual Result: Passed.
        """
        self.assertEqual(time_utils.parse_timecode("1:2:3"), 0.0)