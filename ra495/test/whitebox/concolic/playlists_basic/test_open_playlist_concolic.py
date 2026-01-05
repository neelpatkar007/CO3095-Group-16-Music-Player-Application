import unittest
from unittest.mock import MagicMock, patch
from music_player.playlists_basic import open_playlist


class TestConcolicOpenPlaylist(unittest.TestCase):
    def setUp(self):
        self.S1 = MagicMock()

    @patch('music_player.playlists_basic._activate_playlist_queue')
    @patch('music_player.playlists_basic._print_playlist_contents')
    @patch('music_player.playlists_basic._resolve_playlist')
    @patch('music_player.playlists_basic._ensure_playlists')
    def test_iter1_neg_path(self, mock_ensure, mock_resolve, mock_print_contents, mock_activate):
        S2 = "invalid_id"
        mock_resolve.return_value = None


        open_playlist(self.S1, S2)

        mock_resolve.assert_called_with(self.S1, S2)
        mock_activate.assert_not_called()

    @patch('music_player.playlists_basic._activate_playlist_queue')
    @patch('music_player.playlists_basic._print_playlist_contents')
    @patch('music_player.playlists_basic._resolve_playlist')
    @patch('music_player.playlists_basic._ensure_playlists')
    @patch('builtins.print')
    def test_iter2_pos_path(self, mock_print, mock_ensure, mock_resolve, mock_print_contents, mock_activate):
        S2 = "valid_id"
        mock_pl = MagicMock()
        mock_pl.name = "Concolic Generated Playlist"

        mock_resolve.return_value = mock_pl

        open_playlist(self.S1, S2)

        mock_resolve.assert_called_with(self.S1, S2)
        mock_print.assert_called_with(f"[pl] Opened playlist '{mock_pl.name}':")
        mock_activate.assert_called_once()


if __name__ == '__main__':
    unittest.main()