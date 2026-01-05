import unittest
from unittest.mock import MagicMock, patch
from music_player.playlists_basic import play_playlist

class TestSymbolicExecution(unittest.TestCase):

    def setUp(self):
        self.S1 = MagicMock()
        self.S2 = "symbolic_selector"

    @patch('music_player.playlists_basic._activate_playlist_queue')
    @patch('music_player.playlists_basic._resolve_playlist')
    @patch('music_player.playlists_basic._ensure_playlists')
    def test_PC_1_early_return_when_playlist_is_none(self, mock_ensure, mock_resolve, mock_activate):
        """
        Symbolic Path PC_1:
        Condition: _resolve_playlist(S1, S2) IS None
        Expected Behaviour: Early return, _activate_playlist_queue is NOT called.
        """

        mock_resolve.return_value = None


        play_playlist(self.S1, self.S2)


        mock_ensure.assert_called_once_with(self.S1)
        mock_resolve.assert_called_once_with(self.S1, self.S2)
        mock_activate.assert_not_called()

    @patch('music_player.playlists_basic._activate_playlist_queue')
    @patch('music_player.playlists_basic._resolve_playlist')
    @patch('music_player.playlists_basic._ensure_playlists')
    def test_PC_2_activate_queue_when_playlist_resolved(self, mock_ensure, mock_resolve, mock_activate):
        symbolic_pl = MagicMock()
        mock_resolve.return_value = symbolic_pl

        play_playlist(self.S1, self.S2)

        mock_ensure.assert_called_once_with(self.S1)
        mock_resolve.assert_called_once_with(self.S1, self.S2)
        mock_activate.assert_called_once_with(self.S1, symbolic_pl, auto_play=True)

if __name__ == '__main__':
    unittest.main()