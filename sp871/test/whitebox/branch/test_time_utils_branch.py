import unittest
from music_player import time_utils


class TestTimeUtilsBranch(unittest.TestCase):


    def test_format_branches(self):

        # Branch True (None)
        self.assertEqual(time_utils.format_mm_ss(None), "??:??")
        # Branch True (Negative)
        self.assertEqual(time_utils.format_mm_ss(-1), "??:??")
        # Branch False
        self.assertEqual(time_utils.format_mm_ss(10), "00:10")

    def test_parse_type_and_empty_branches(self):

        # Bytes Check
        time_utils.parse_timecode(b"10")  # True
        time_utils.parse_timecode("10")  # False

        # Empty Check
        time_utils.parse_timecode("")  # True
        time_utils.parse_timecode("10")  # False

    def test_parse_colon_branches(self):

        # Colon Check
        time_utils.parse_timecode("1:00")  # True
        time_utils.parse_timecode("60")  # False

        # Length Check
        time_utils.parse_timecode("1:00:00")  # True
        time_utils.parse_timecode("1:00")  # False

    def test_parse_negative_and_exception_branches(self):

        # Negative Check
        time_utils.parse_timecode("-10")  # True
        time_utils.parse_timecode("10")  # False

        # Exception Branch
        time_utils.parse_timecode("invalid")
        time_utils.parse_timecode("10")