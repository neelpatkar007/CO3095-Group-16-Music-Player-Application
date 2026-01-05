import unittest
from unittest.mock import MagicMock, patch
import datetime
from music_player.player_time import show_recently_added


class TestSymbolicExecution(unittest.TestCase):


    def test_path_pc1(self):
        s1 = None
        self.assertIsNone(show_recently_added(s1))

    def test_path_pc2(self):
        s1 = MagicMock()
        s1.library_tracks = None
        with patch('builtins.print') as mocked_print:
            show_recently_added(s1)
            mocked_print.assert_any_call("[recent] Library is empty.")

    def test_path_pc4(self):
        s1 = MagicMock()
        track = MagicMock()
        track.path = None
        s1.library_tracks = [track]

        with patch('builtins.print') as mocked_print:
            show_recently_added(s1)
            mocked_print.assert_any_call("[recent] No valid files found.")


if __name__ == '__main__':
    unittest.main()