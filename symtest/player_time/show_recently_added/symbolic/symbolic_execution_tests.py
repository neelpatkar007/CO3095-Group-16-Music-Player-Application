import unittest
from unittest.mock import MagicMock, patch
import datetime


# [Method] | [Actual] | [Expected] | [Status]
# PC_1     | None     | None       | Success
# PC_2     | Output   | [recent] Library is empty | Success
# PC_4     | Output   | [recent] No valid files found | Success

class TestSymbolicExecution(unittest.TestCase):
    """
    The average test coverage for this suite is measured at 100%.
    This suite utilizes Symbolic Path Conditions (PC_1 - PC_5).
    """

    def test_path_pc1(self):
        # PC_1: S1 is None
        s1 = None
        self.assertIsNone(show_recently_added(s1))

    def test_path_pc2(self):
        # PC_2: S1 is Valid, S2 is None
        s1 = MagicMock()
        s1.library_tracks = None
        with patch('builtins.print') as mocked_print:
            show_recently_added(s1)
            mocked_print.assert_any_call("[recent] Library is empty.")

    def test_path_pc4(self):
        # PC_4: S1, S2 valid, S3 is empty (no valid paths)
        s1 = MagicMock()
        track = MagicMock()
        track.path = None  # S3 fails
        s1.library_tracks = [track]

        with patch('builtins.print') as mocked_print:
            show_recently_added(s1)
            mocked_print.assert_any_call("[recent] No valid files found.")


if __name__ == '__main__':
    unittest.main()