import unittest
from music_player import time_utils


class TestTimeUtilsStatement(unittest.TestCase):


    def test_format_statements(self):

        # Early Return
        time_utils.format_mm_ss(None)

        # Calculation
        res = time_utils.format_mm_ss(65)
        self.assertEqual(res, "01:05")

    def test_parse_decoding_and_empty(self):

        # Bytes decoding
        self.assertEqual(time_utils.parse_timecode(b"60"), 60.0)

        # Empty string
        self.assertEqual(time_utils.parse_timecode("   "), 0.0)

    def test_parse_complex_logic(self):

        # MM:SS
        time_utils.parse_timecode("1:30")

        # Negative
        time_utils.parse_timecode("-10")

        # Exception Handler
        res = time_utils.parse_timecode("abc")
        self.assertEqual(res, 0.0)

    def test_parse_split_validation(self):

        self.assertEqual(time_utils.parse_timecode("1:2:3"), 0.0)