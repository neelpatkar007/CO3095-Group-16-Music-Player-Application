import unittest
from unittest.mock import MagicMock, patch
from music_player import playlists_advanced
from music_player.player_state import PlayerState


class TestPlaylistsAdvancedBranch(unittest.TestCase):
    """
    White-Box Branch Tests for playlists_advanced.py.
    Tools: Python unittest + unittest.mock
    Technique: White-Box Branch Testing
    """

    def setUp(self):
        self.pl1 = MagicMock();
        self.pl1.name = "One"
        self.pl2 = MagicMock();
        self.pl2.name = "Two"
        self.state = PlayerState([], MagicMock())
        self.state.playlists = [self.pl1, self.pl2]

    def test_get_playlist_index_branches(self):
        """
        Expected Result:
         - Returns correct playlist for valid digit strings.
         - Returns None and prints error for indices < 0 or >= list length.
        Actual Result: Passed. Verified index logic branches.
        """
        # Digit Valid Index
        res = playlists_advanced._get_playlist(self.state, "1")
        self.assertEqual(res, self.pl1)

        # Digit Invalid Index
        with patch("builtins.print") as mock_print:
            res = playlists_advanced._get_playlist(self.state, "0")
            self.assertIsNone(res)
            mock_print.assert_called()

        # Digit Invalid Index
        with patch("builtins.print") as mock_print:
            res = playlists_advanced._get_playlist(self.state, "99")
            self.assertIsNone(res)
            mock_print.assert_called()