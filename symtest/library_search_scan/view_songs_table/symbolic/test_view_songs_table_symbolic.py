import unittest
from unittest.mock import MagicMock, patch
from music_player.player_state import PlayerState
from music_player.library_search_scan import view_songs_table

class TestSymbolicExecution(unittest.TestCase):
    @patch('music_player.library_search_scan._print_tracks_table')
    @patch('music_player.library_search_scan.print')

    def test_pc1_state_none(self, mock_print, mock_print_tracks):
        s1_input = None
        view_songs_table(s1_input)

        calls = [str(call[0][0]) for call in mock_print.call_args_list]
        self.assertIn("[lib] --- All Songs ---", calls)
        self.assertTrue(any("(empty library)" in call for call in calls))
        mock_print_tracks.assert_not_called()

    @patch('music_player.library_search_scan._print_tracks_table')
    @patch('music_player.library_search_scan.print')
    def test_pc2_state_exists_lib_empty(self, mock_print, mock_print_tracks):
        mock_audio_engine = MagicMock()
        s1_input = PlayerState(tracks=[], audio_engine=mock_audio_engine)

        view_songs_table(s1_input)

        calls = [str(call[0][0]) for call in mock_print.call_args_list]
        self.assertTrue(any("(empty library)" in call for call in calls))
        mock_print_tracks.assert_not_called()

    @patch('music_player.library_search_scan._print_tracks_table')
    @patch('music_player.library_search_scan.print')
    def test_pc3_state_exists_lib_full(self, mock_print, mock_print_tracks):
        mock_audio_engine = MagicMock()
        s1_input = PlayerState(tracks=[], audio_engine=mock_audio_engine)

        track_a = MagicMock()
        track_a.duration_seconds = 120
        track_b = MagicMock()
        track_b.duration_seconds = 180
        s1_input.library_tracks = [track_a, track_b]

        view_songs_table(s1_input)

        calls = [str(call[0][0]) for call in mock_print.call_args_list]
        self.assertIn("[lib] --- All Songs ---", calls)
        mock_print_tracks.assert_called_once_with([track_a, track_b])


if __name__ == '__main__':
    unittest.main()