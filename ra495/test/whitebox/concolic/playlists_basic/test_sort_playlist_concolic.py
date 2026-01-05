import unittest
from unittest.mock import MagicMock, patch
from music_player.playlists_basic import sort_playlist
from music_player.playlists_basic import _resolve_playlist

class TestConcolicGenerations(unittest.TestCase):

    def setUp(self):
        self.mock_state = MagicMock()

    @patch('builtins.print')
    def test_iter_1_pc1(self, mock_print):
        S1, S2, S3 = None, "sel", "title"
        sort_playlist(S1, S2, S3)
        mock_print.assert_called_with("[pl] Error: State is None.")

    @patch('builtins.print')
    def test_iter_2_pc2(self, mock_print):
        S1, S2, S3 = self.mock_state, "", "title"
        sort_playlist(S1, S2, S3)
        mock_print.assert_called_with("[pl] Error: Selector cannot be empty.")

    @patch('builtins.print')
    def test_iter_3_pc3(self, mock_print):
        S1, S2, S3 = self.mock_state, "sel", None
        sort_playlist(S1, S2, S3)
        mock_print.assert_called_with("[pl] Error: Sort criteria must be a valid string.")

    @patch('builtins.print')
    @patch('music_player.playlists_basic._resolve_playlist')
    def test_iter_4_pc4(self, mock_resolve, mock_print):
        S1, S2, S3 = self.mock_state, "sel", "title"
        mock_resolve.return_value = None

        sort_playlist(S1, S2, S3)
        self.assertFalse(mock_print.called)

    @patch('builtins.print')
    @patch('music_player.playlists_basic._resolve_playlist')
    def test_iter_5_pc5(self, mock_resolve, mock_print):
        """Iteration 5: Flip S4!=None. Derived Constraint S5 (tracks) is None. Path: PC_5."""
        S1, S2, S3 = self.mock_state, "sel", "title"
        mock_pl = MagicMock()
        mock_pl.tracks = None
        mock_resolve.return_value = mock_pl

        sort_playlist(S1, S2, S3)
        mock_print.assert_called_with("[pl] Error: Playlist tracks corrupted.")

    @patch('builtins.print')
    @patch('music_player.playlists_basic._resolve_playlist')
    def test_iter_6_pc6(self, mock_resolve, mock_print):
        """Iteration 6: Flip S5!=None. Derived Constraint S5 is Empty. Path: PC_6."""
        S1, S2, S3 = self.mock_state, "sel", "title"
        mock_pl = MagicMock()
        mock_pl.tracks = []
        mock_pl.name = "EmptyPL"
        mock_resolve.return_value = mock_pl

        sort_playlist(S1, S2, S3)
        mock_print.assert_called_with("[pl] Playlist 'EmptyPL' is empty, nothing to sort.")

    @patch('builtins.print')
    @patch('music_player.playlists_basic._resolve_playlist')
    def test_iter_7_pc7(self, mock_resolve, mock_print):
        S1, S2, S3 = self.mock_state, "sel", "title"
        mock_pl = MagicMock()
        mock_pl.tracks = [MagicMock(title="B"), MagicMock(title="A")]
        mock_pl.name = "ConcolicPL"
        mock_resolve.return_value = mock_pl

        sort_playlist(S1, S2, S3)
        mock_print.assert_called_with("[pl] Sorted playlist 'ConcolicPL' by title.")

    @patch('builtins.print')
    @patch('music_player.playlists_basic._resolve_playlist')
    def test_iter_8_pc9(self, mock_resolve, mock_print):
        S1, S2, S3 = self.mock_state, "sel", "artist"
        mock_pl = MagicMock()
        mock_pl.tracks = [MagicMock(artist="B"), MagicMock(artist="A")]
        mock_pl.name = "ConcolicPL"
        mock_resolve.return_value = mock_pl

        sort_playlist(S1, S2, S3)
        mock_print.assert_called_with("[pl] Sorted playlist 'ConcolicPL' by artist.")

    @patch('builtins.print')
    @patch('music_player.playlists_basic._resolve_playlist')
    def test_iter_9_pc11(self, mock_resolve, mock_print):
        S1, S2, S3 = self.mock_state, "sel", "duration"
        mock_pl = MagicMock()
        mock_pl.tracks = [MagicMock(duration_seconds=10), MagicMock(duration_seconds=5)]
        mock_pl.name = "ConcolicPL"
        mock_resolve.return_value = mock_pl

        sort_playlist(S1, S2, S3)
        mock_print.assert_called_with("[pl] Sorted playlist 'ConcolicPL' by duration.")

    @patch('builtins.print')
    @patch('music_player.playlists_basic._resolve_playlist')
    def test_iter_10_pc13(self, mock_resolve, mock_print):
        S1, S2, S3 = self.mock_state, "sel", "genre"
        mock_pl = MagicMock()
        mock_pl.tracks = [MagicMock()]
        mock_resolve.return_value = mock_pl

        sort_playlist(S1, S2, S3)
        mock_print.assert_called_with("[pl] Invalid sort criteria. Use: title, artist, duration")