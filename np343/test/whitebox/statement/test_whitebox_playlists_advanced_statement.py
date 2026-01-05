import unittest
from unittest.mock import MagicMock, patch
from music_player import playlists_advanced
from music_player.player_state import PlayerState

class TestPlaylistsAdvancedStatement(unittest.TestCase):

    def setUp(self):
        self.state = PlayerState([], MagicMock())
        self.pl1 = MagicMock()
        self.pl1.name = "One"
        self.state.playlists = [self.pl1]

    def test_get_playlist_helper_errors(self):
        with patch("builtins.print") as mock_print:
            res = playlists_advanced._get_playlist(None, "MyMix")
            self.assertIsNone(res)
            mock_print.assert_called()

        with patch("builtins.print") as mock_print:
            res = playlists_advanced._get_playlist(self.state, "   ")
            self.assertIsNone(res)
            mock_print.assert_called()

    def test_merge_playlists_source_missing(self):
        dest_pl = MagicMock()
        dest_pl.name = "Dest"
        self.state.playlists = [dest_pl]

        with patch("music_player.playlists_advanced._get_playlist", side_effect=[dest_pl, None]):
            with patch("builtins.print") as mock_print:
                playlists_advanced.merge_playlists(self.state, "Dest", "Missing")

    def test_copy_playlist_warnings(self):
        with patch("builtins.print") as mock_print:
            playlists_advanced.copy_playlist(self.state, "One", "admin")
            mock_print.assert_called_with("[pl] Error: That name is reserved.")

        with patch("music_player.playlists_advanced._get_playlist", return_value=None):
            playlists_advanced.copy_playlist(self.state, "Ghost", "NewMix")

    def test_copy_empty_source_warning(self):
        empty_pl = MagicMock()
        empty_pl.name = "EmptySource"
        empty_pl.tracks = []  # Empty

        self.state.playlists = [empty_pl]

        with patch("music_player.playlists_advanced._get_playlist", return_value=empty_pl):
            with patch("builtins.print") as mock_print:
                playlists_advanced.copy_playlist(self.state, "EmptySource", "NewCopy")
                args = mock_print.call_args[0][0]
                self.assertTrue(len(mock_print.call_args_list) > 0)