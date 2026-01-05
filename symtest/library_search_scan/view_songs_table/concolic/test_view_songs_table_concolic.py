import unittest
from unittest.mock import MagicMock, patch
from music_player.player_state import PlayerState
from music_player.library_search_scan import view_songs_table

class TestConcolicExecution(unittest.TestCase):

    @patch('music_player.library_search_scan._print_tracks_table')
    @patch('music_player.library_search_scan.print')
    def test_iteration_1_seed_degenerate(self, mock_print, mock_print_tracks):
        s1 = None
        view_songs_table(s1)
        calls = [str(call[0][0]) for call in mock_print.call_args_list]
        self.assertTrue(any("(empty library)" in call for call in calls))
        mock_print_tracks.assert_not_called()

    @patch('music_player.library_search_scan._print_tracks_table')
    @patch('music_player.library_search_scan.print')
    def test_iteration_2_flip_s1(self, mock_print, mock_print_tracks):
        mock_audio_engine = MagicMock()
        s1 = PlayerState(tracks=[], audio_engine=mock_audio_engine)

        view_songs_table(s1)

        calls = [str(call[0][0]) for call in mock_print.call_args_list]
        self.assertTrue(any("(empty library)" in call for call in calls))
        mock_print_tracks.assert_not_called()

    @patch('music_player.library_search_scan._print_tracks_table')
    @patch('music_player.library_search_scan.print')
    def test_iteration_3_flip_s2(self, mock_print, mock_print_tracks):
        mock_audio_engine = MagicMock()
        s1 = PlayerState(tracks=[], audio_engine=mock_audio_engine)

        track = MagicMock()
        track.duration_seconds = 120
        s1.library_tracks = [track]

        view_songs_table(s1)

        calls = [str(call[0][0]) for call in mock_print.call_args_list]
        self.assertFalse(any("(empty library)" in call for call in calls))
        mock_print_tracks.assert_called_once()


if __name__ == '__main__':
    unittest.main()