import unittest
from unittest.mock import MagicMock, patch, call
from music_player.playlists_basic import open_playlist

class TestSymbolicOpenPlaylist(unittest.TestCase):

    def setUp(self):
        self.S1 = MagicMock()
        self.S2 = "test_selector"

    @patch('music_player.playlists_basic._activate_playlist_queue')
    @patch('music_player.playlists_basic._print_playlist_contents')
    @patch('music_player.playlists_basic._resolve_playlist')
    @patch('music_player.playlists_basic._ensure_playlists')
    @patch('builtins.print')
    def test_pc1_not_found(self, mock_print, mock_ensure, mock_resolve, mock_print_contents, mock_activate):
        mock_resolve.return_value = None


        open_playlist(self.S1, self.S2)

        mock_ensure.assert_called_once_with(self.S1)
        mock_resolve.assert_called_once_with(self.S1, self.S2)

        mock_print.assert_not_called()
        mock_print_contents.assert_not_called()
        mock_activate.assert_not_called()

    @patch('music_player.playlists_basic._activate_playlist_queue')
    @patch('music_player.playlists_basic._print_playlist_contents')
    @patch('music_player.playlists_basic._resolve_playlist')
    @patch('music_player.playlists_basic._ensure_playlists')
    @patch('builtins.print')
    def test_pc2_success(self, mock_print, mock_ensure, mock_resolve, mock_print_contents, mock_activate):

        mock_pl = MagicMock()
        mock_pl.name = "Summer Hits"
        mock_resolve.return_value = mock_pl


        open_playlist(self.S1, self.S2)

        mock_ensure.assert_called_once_with(self.S1)
        mock_resolve.assert_called_once_with(self.S1, self.S2)

        mock_print.assert_called_with("[pl] Opened playlist 'Summer Hits':")
        mock_print_contents.assert_called_once_with(mock_pl)
        mock_activate.assert_called_once_with(self.S1, mock_pl, auto_play=True)


if __name__ == '__main__':
    unittest.main()