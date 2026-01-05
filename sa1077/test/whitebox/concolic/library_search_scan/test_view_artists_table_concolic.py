import unittest
from unittest.mock import MagicMock, patch
from music_player.player_state import PlayerState
from music_player.library_search_scan import view_artists_table

class TestConcolicGenerative(unittest.TestCase):

    @patch('music_player.library_search_scan.print')
    def test_iter1_seed_none(self, mock_print):
        S1 = None
        view_artists_table(S1)
        mock_print.assert_not_called()

    @patch('music_player.library_search_scan.print')
    def test_iter2_seed_obj_no_attr(self, mock_print):
        S1 = MagicMock(spec=[])
        view_artists_table(S1)
        mock_print.assert_called_with("[lib] Error: Library unavailable.")

    @patch('music_player.library_search_scan.print')
    def test_iter3_seed_empty_list(self, mock_print):
        mock_audio_engine = MagicMock()
        S1 = PlayerState(tracks=[], audio_engine=mock_audio_engine)
        view_artists_table(S1)
        mock_print.assert_called_with("  (no artists found)")

    @patch('music_player.library_search_scan.print')
    def test_iter4_seed_list_none(self, mock_print):
        mock_audio_engine = MagicMock()
        S1 = PlayerState(tracks=[], audio_engine=mock_audio_engine)
        S1.library_tracks = [None]
        view_artists_table(S1)
        mock_print.assert_called_with("  (no artists found)")

    @patch('music_player.library_search_scan.print')
    def test_iter5_seed_no_artist_attr(self, mock_print):
        mock_audio_engine = MagicMock()
        S1 = PlayerState(tracks=[], audio_engine=mock_audio_engine)
        t = MagicMock(spec=['duration_seconds'])
        t.duration_seconds = 120
        S1.library_tracks = [t]

        view_artists_table(S1)
        full_output = "\n".join([c[0][0] for c in mock_print.call_args_list])
        self.assertIn("Unknown", full_output)

    @patch('music_player.library_search_scan.print')
    def test_iter6_seed_artist_none(self, mock_print):
        mock_audio_engine = MagicMock()
        S1 = PlayerState(tracks=[], audio_engine=mock_audio_engine)
        t = MagicMock()
        t.artist = None
        t.duration_seconds = 120
        S1.library_tracks = [t]

        view_artists_table(S1)
        full_output = "\n".join([c[0][0] for c in mock_print.call_args_list])
        self.assertIn("Unknown", full_output)

    @patch('music_player.library_search_scan.print')
    def test_iter7_seed_artist_empty(self, mock_print):
        mock_audio_engine = MagicMock()
        S1 = PlayerState(tracks=[], audio_engine=mock_audio_engine)
        t = MagicMock()
        t.artist = "   "  # Whitespace
        t.duration_seconds = 120
        S1.library_tracks = [t]

        view_artists_table(S1)
        full_output = "\n".join([c[0][0] for c in mock_print.call_args_list])
        self.assertIn("Unknown", full_output)

    @patch('music_player.library_search_scan.print')
    def test_iter8_seed_valid_artist(self, mock_print):
        mock_audio_engine = MagicMock()
        S1 = PlayerState(tracks=[], audio_engine=mock_audio_engine)
        t = MagicMock()
        t.artist = "Mozart"
        t.duration_seconds = 120
        S1.library_tracks = [t]

        view_artists_table(S1)
        full_output = "\n".join([c[0][0] for c in mock_print.call_args_list])
        self.assertIn("Mozart", full_output)


if __name__ == '__main__':
    unittest.main()