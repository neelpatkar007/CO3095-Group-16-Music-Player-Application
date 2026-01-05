import unittest
from unittest.mock import MagicMock, patch
from music_player.library_search_scan import _print_tracks_table

class TestSymbolicExecution(unittest.TestCase):
    @patch('music_player.library_search_scan.print')
    def test_pc1_empty_list_constraint(self, mock_print):
        s1_tracks = []
        _print_tracks_table(s1_tracks)
        mock_print.assert_called_with("  (no tracks)")

    @patch('music_player.library_search_scan.format_mm_ss')
    @patch('music_player.library_search_scan.print')
    def test_pc2_list_with_none_element(self, mock_print, mock_format):
        s1_tracks = [None]
        _print_tracks_table(s1_tracks)
        self.assertTrue(mock_print.call_count >= 2)
        mock_format.assert_not_called()

    @patch('music_player.library_search_scan.format_mm_ss')
    @patch('music_player.library_search_scan.print')
    def test_pc3_valid_track_processing(self, mock_print, mock_format):
        mock_format.return_value = "03:30"
        s2_track = MagicMock()
        s2_track.title = "Bohemian Rhapsody"
        s2_track.artist = "Queen"
        s2_track.duration_seconds = 354
        s1_tracks = [s2_track]
        _print_tracks_table(s1_tracks)
        last_print_call = mock_print.call_args[0][0]
        self.assertIn("Bohemian Rhapsody", last_print_call)
        self.assertIn("Queen", last_print_call)
        self.assertIn("03:30", last_print_call)


if __name__ == '__main__':
    unittest.main()