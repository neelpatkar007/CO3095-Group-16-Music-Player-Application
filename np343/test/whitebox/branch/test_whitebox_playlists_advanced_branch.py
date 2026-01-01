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

    def test_copy_name_validation_branches(self):
        """
        Expected Result:
         - 1. Prints error if name < 3 chars.
         - 2. Prints error if name > 20 chars.
         - 3. Prints error if name contains non-alphanumeric characters.
        Actual Result: Passed. Verified all three validation branches trigger error messages.
        """
        # Name too short
        with patch("builtins.print") as mock_print:
            playlists_advanced.copy_playlist(self.state, "One", "Hi")
            mock_print.assert_called()

        # Name too long
        with patch("builtins.print") as mock_print:
            playlists_advanced.copy_playlist(self.state, "One", "A" * 21)
            mock_print.assert_called()

        # Invalid Chars
        with patch("builtins.print") as mock_print:
            playlists_advanced.copy_playlist(self.state, "One", "My Mix!")
            mock_print.assert_called()
