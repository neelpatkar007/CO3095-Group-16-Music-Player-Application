import unittest
from unittest.mock import MagicMock, patch
from music_player.playlists_basic import sort_playlist


class TestSymbolicExecution(unittest.TestCase):

    def setUp(self):
        self.mock_state = MagicMock()

    @patch('builtins.print')
    def test_PC1_state_none(self, mock_print):
        sort_playlist(None, "valid_sel", "title")

        mock_print.assert_called_with("[pl] Error: State is None.")

    @patch('builtins.print')
    def test_PC2_selector_empty(self, mock_print):
        S1 = self.mock_state
        S2_variants = [None, "", "   "]

        for S2 in S2_variants:
            sort_playlist(S1, S2, "title")
            mock_print.assert_called_with("[pl] Error: Selector cannot be empty.")

    @patch('builtins.print')
    def test_PC3_criteria_invalid(self, mock_print):
        S1 = self.mock_state
        S2 = "valid_selector"
        S3_variants = [None, 123, ""]

        for S3 in S3_variants:
            sort_playlist(S1, S2, S3)
            mock_print.assert_called_with("[pl] Error: Sort criteria must be a valid string.")

    @patch('builtins.print')
    @patch('music_player.playlists_basic._resolve_playlist')
    def test_PC4_resolve_returns_none(self, mock_resolve, mock_print):
        S1 = self.mock_state
        S2 = "valid_selector"
        S3 = "title"

        mock_resolve.return_value = None

        sort_playlist(S1, S2, S3)

        self.assertFalse(mock_print.called or "Error" in str(mock_print.call_args))

    @patch('builtins.print')
    @patch('music_player.playlists_basic._resolve_playlist')
    def test_PC5_tracks_corrupted(self, mock_resolve, mock_print):
        S1 = self.mock_state
        S2 = "valid_selector"
        S3 = "title"

        mock_pl_a = MagicMock()
        mock_pl_a.tracks = None
        mock_resolve.return_value = mock_pl_a
        sort_playlist(S1, S2, S3)
        mock_print.assert_called_with("[pl] Error: Playlist tracks corrupted.")

        mock_pl_b = MagicMock()
        del mock_pl_b.tracks
        mock_resolve.return_value = mock_pl_b
        sort_playlist(S1, S2, S3)
        mock_print.assert_called_with("[pl] Error: Playlist tracks corrupted.")

    @patch('builtins.print')
    @patch('music_player.playlists_basic._resolve_playlist')
    def test_PC6_tracks_empty(self, mock_resolve, mock_print):
        """Path Condition 6: S5 is empty list."""
        S1 = self.mock_state
        S2 = "valid_selector"
        S3 = "title"

        mock_pl = MagicMock()
        mock_pl.tracks = []
        mock_pl.name = "TestPL"
        mock_resolve.return_value = mock_pl

        sort_playlist(S1, S2, S3)
        mock_print.assert_called_with("[pl] Playlist 'TestPL' is empty, nothing to sort.")

    @patch('builtins.print')
    @patch('music_player.playlists_basic._resolve_playlist')
    def test_PC7_sort_title_success(self, mock_resolve, mock_print):
        S1 = self.mock_state
        S2 = "valid_selector"
        S3 = "TiTlE "

        track1 = MagicMock(title="B Song")
        track2 = MagicMock(title="A Song")
        mock_pl = MagicMock()
        mock_pl.tracks = [track1, track2]
        mock_pl.name = "TestPL"
        mock_resolve.return_value = mock_pl

        sort_playlist(S1, S2, S3)

        self.assertEqual(mock_pl.tracks, [track2, track1])
        mock_print.assert_called_with("[pl] Sorted playlist 'TestPL' by title.")

    @patch('builtins.print')
    @patch('music_player.playlists_basic._resolve_playlist')
    def test_PC8_sort_title_exception(self, mock_resolve, mock_print):
        S1 = self.mock_state
        S2 = "valid_selector"
        S3 = "title"

        mock_pl = MagicMock()

        mock_pl.tracks.sort.side_effect = Exception("SortFail")
        mock_resolve.return_value = mock_pl

        sort_playlist(S1, S2, S3)
        mock_print.assert_called_with("[pl] Error sorting by title: SortFail")

    @patch('builtins.print')
    @patch('music_player.playlists_basic._resolve_playlist')
    def test_PC9_sort_artist_success(self, mock_resolve, mock_print):
        S1 = self.mock_state
        S2 = "valid_selector"
        S3 = "artist"

        track1 = MagicMock(artist="Zebra")
        track2 = MagicMock(artist="Abba")
        mock_pl = MagicMock()
        mock_pl.tracks = [track1, track2]
        mock_pl.name = "TestPL"
        mock_resolve.return_value = mock_pl

        sort_playlist(S1, S2, S3)
        self.assertEqual(mock_pl.tracks, [track2, track1])
        mock_print.assert_called_with("[pl] Sorted playlist 'TestPL' by artist.")

    @patch('builtins.print')
    @patch('music_player.playlists_basic._resolve_playlist')
    def test_PC10_sort_artist_exception(self, mock_resolve, mock_print):
        mock_pl = MagicMock()
        mock_pl.tracks.sort.side_effect = Exception("ArtistFail")
        mock_resolve.return_value = mock_pl

        sort_playlist(self.mock_state, "sel", "artist")
        mock_print.assert_called_with("[pl] Error sorting by artist: ArtistFail")

    @patch('builtins.print')
    @patch('music_player.playlists_basic._resolve_playlist')
    def test_PC11_sort_duration_success(self, mock_resolve, mock_print):
        S1 = self.mock_state
        S2 = "valid_selector"
        S3 = "duration"

        track1 = MagicMock(duration_seconds=300)
        track2 = MagicMock(duration_seconds=100)
        mock_pl = MagicMock()
        mock_pl.tracks = [track1, track2]
        mock_pl.name = "TestPL"
        mock_resolve.return_value = mock_pl

        sort_playlist(S1, S2, S3)
        self.assertEqual(mock_pl.tracks, [track2, track1])
        mock_print.assert_called_with("[pl] Sorted playlist 'TestPL' by duration.")

    @patch('builtins.print')
    @patch('music_player.playlists_basic._resolve_playlist')
    def test_PC12_sort_duration_exception(self, mock_resolve, mock_print):
        mock_pl = MagicMock()
        mock_pl.tracks.sort.side_effect = Exception("DurFail")
        mock_resolve.return_value = mock_pl

        sort_playlist(self.mock_state, "sel", "duration")
        mock_print.assert_called_with("[pl] Error sorting by duration: DurFail")

    @patch('builtins.print')
    @patch('music_player.playlists_basic._resolve_playlist')
    def test_PC13_invalid_criteria(self, mock_resolve, mock_print):
        S1 = self.mock_state
        S2 = "valid_selector"
        S3 = "genre"

        mock_pl = MagicMock()
        mock_pl.tracks = [MagicMock()]
        mock_resolve.return_value = mock_pl

        sort_playlist(S1, S2, S3)
        mock_print.assert_called_with("[pl] Invalid sort criteria. Use: title, artist, duration")


if __name__ == '__main__':
    import sys
    from unittest.mock import MagicMock

    module_name = 'function_source'
    sys.modules[module_name] = MagicMock()

    pass