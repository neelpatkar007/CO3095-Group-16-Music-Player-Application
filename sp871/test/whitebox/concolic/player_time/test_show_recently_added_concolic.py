import unittest
from unittest.mock import MagicMock, patch
import datetime
from music_player.player_time import show_recently_added


class TestConcolicTesting(unittest.TestCase):


    def test_path_pc3_exception(self):
        s1 = MagicMock()
        track = MagicMock()
        track.path.exists.return_value = True
        # Accessing stat triggers the S4 symbolic exception
        track.path.stat.side_effect = PermissionError()
        s1.library_tracks = [track]

        with patch('builtins.print') as mocked_print:
            show_recently_added(s1)
            mocked_print.assert_any_call("[recent] Permission denied whilst accessing track metadata.")

    def test_path_pc5_full_execution(self):
        # PC_5: Full success path
        s1 = MagicMock()
        track = MagicMock()
        track.path.exists.return_value = True
        track.path.stat.return_value.st_mtime = 1000000
        track.display_name = "Test Track"
        s1.library_tracks = [track]

        with patch('builtins.print') as mocked_print:
            show_recently_added(s1)
            # Verify the header was printed (PC_5 entry)
            mocked_print.assert_any_call("--- Recently Added Songs ---")
            # Verify loop output
            mocked_print.assert_any_call("  1. [1970-01-12] Test Track")

if __name__ == '__main__':
    unittest.main()