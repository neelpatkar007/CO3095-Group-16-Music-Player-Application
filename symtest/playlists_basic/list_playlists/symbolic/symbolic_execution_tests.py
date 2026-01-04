import unittest
from unittest.mock import MagicMock, patch
from io import StringIO
import sys
from music_player.playlists_basic import list_playlists


class TestSymbolicExecution(unittest.TestCase):
    """
    White-Box Symbolic Testing Suite for list_playlists.
    """

    def setUp(self):
        self.captured_output = StringIO()
        sys.stdout = self.captured_output
        self.mock_ensure = patch('music_player.playlists_basic._ensure_playlists').start()
        self.mock_summary = patch('music_player.playlists_basic._get_playlist_summary').start()
        self.mock_format = patch('music_player.playlists_basic.format_mm_ss').start()

    def tearDown(self):
        patch.stopall()
        sys.stdout = sys.__stdout__

    def test_pc1_state_none(self):
        """PC_1: S1 is None."""
        list_playlists(None)
        output = self.captured_output.getvalue().strip()
        self.assertEqual(output, "[pl] Internal Error: State is missing.")

    def test_pc2_playlists_attr_none(self):
        """PC_2: S1 is NOT None AND S2 is None."""
        S1 = MagicMock()
        del S1.playlists
        object.__setattr__(S1, 'playlists', None)
        list_playlists(S1)
        output = self.captured_output.getvalue().strip()
        self.assertEqual(output, "")

    def test_pc3_playlists_not_list(self):
        """PC_3: S1 is NOT None AND S3 (IsInstance List) is False."""
        S1 = MagicMock()
        S1.playlists = "CorruptedString"
        list_playlists(S1)
        output = self.captured_output.getvalue().strip()
        self.assertEqual(output, "[pl] Error: Playlist data is corrupted.")

    def test_pc4_playlists_empty(self):
        """PC_4: S1 is NOT None AND S3 is True AND S4 (len > 0) is False."""
        S1 = MagicMock()
        S1.playlists = []
        list_playlists(S1)
        output = self.captured_output.getvalue().strip()
        self.assertEqual(output, "[pl] No playlists defined.")

    def test_pc5_playlist_item_none(self):
        """PC_5: ... AND S5 (Item) is None."""
        S1 = MagicMock()
        S1.playlists = [None]
        list_playlists(S1)
        output = self.captured_output.getvalue()
        self.assertIn("<Error: Invalid Playlist>", output)

    def test_pc6_item_valid_not_active(self):
        """PC_6: ... AND S5 Valid AND S6 (Active Index) mismatch/None."""
        S1 = MagicMock()
        pl_mock = MagicMock()
        pl_mock.name = "Chill Vibes"
        S1.playlists = [pl_mock]
        S1.active_playlist_index = 99
        self.mock_summary.return_value = (5, 300)
        self.mock_format.return_value = "05:00"
        list_playlists(S1)
        output = self.captured_output.getvalue()
        self.assertIn("1. Chill Vibes ", output)
        self.assertNotIn("*", output)
        self.assertIn("5 songs", output)

    def test_pc7_item_valid_active_singular(self):
        """PC_7: ... AND S5 Valid AND S6 matches AND S8 (Count) is 1."""
        S1 = MagicMock()
        pl_mock = MagicMock()
        pl_mock.name = "Solo Track"
        S1.playlists = [pl_mock]
        S1.active_playlist_index = 0
        self.mock_summary.return_value = (1, 60)
        self.mock_format.return_value = "01:00"
        list_playlists(S1)
        output = self.captured_output.getvalue()
        self.assertIn("1. Solo Track*", output)
        self.assertIn("1 song,", output)


if __name__ == '__main__':
    unittest.main()
