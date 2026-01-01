import unittest
from unittest.mock import MagicMock, patch
from music_player import playlists_advanced
from music_player.player_state import PlayerState

class TestPlaylistsAdvancedStatement(unittest.TestCase):
    """
    White-Box Statement Coverage for playlists_advanced.py.
    Targets: Missing error blocks in _get_playlist and copy/merge validations.
    """

    def setUp(self):
        self.state = PlayerState([], MagicMock())
        # Populate playlists to pass initial availability checks
        self.pl1 = MagicMock()
        self.pl1.name = "One"
        self.state.playlists = [self.pl1]

    def test_get_playlist_helper_errors(self):
        """
        Expected Result: Helper returns None and prints specific error messages when state is invalid or selector is empty strings.
        Actual Result: Passed. Verified None return and presence of error prints.
        """
        # State invalid
        with patch("builtins.print") as mock_print:
            res = playlists_advanced._get_playlist(None, "MyMix")
            self.assertIsNone(res)
            mock_print.assert_called()

        # Selector empty
        with patch("builtins.print") as mock_print:
            res = playlists_advanced._get_playlist(self.state, "   ")
            self.assertIsNone(res)
            mock_print.assert_called()

    def test_merge_playlists_source_missing(self):
        """
        Expected Result: Function returns early without crashing if the source playlist cannot be resolved.
        Actual Result: Passed. Silent return after helper failure.
        """
        # Logic requires valid destination to reach source check
        dest_pl = MagicMock()
        dest_pl.name = "Dest"
        self.state.playlists = [dest_pl]

        # Force _get_playlist to return None
        with patch("music_player.playlists_advanced._get_playlist", side_effect=[dest_pl, None]):
            with patch("builtins.print") as mock_print:
                playlists_advanced.merge_playlists(self.state, "Dest", "Missing")