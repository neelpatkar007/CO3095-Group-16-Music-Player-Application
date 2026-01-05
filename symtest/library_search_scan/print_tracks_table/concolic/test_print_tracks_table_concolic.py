import unittest
from unittest.mock import MagicMock, patch
from types import SimpleNamespace
from music_player.library_search_scan import _print_tracks_table

class TestConcolicExecution(unittest.TestCase):

    @patch('music_player.library_search_scan.print')
    def test_iteration_1_base_constraint(self, mock_print):
        s1_tracks = []
        _print_tracks_table(s1_tracks)
        mock_print.assert_called_with("  (no tracks)")

    @patch('music_player.library_search_scan.format_mm_ss')
    @patch('music_player.library_search_scan.print')
    def test_iteration_2_negated_list_constraint(self, mock_print, mock_format):
        s1_tracks = [None]
        _print_tracks_table(s1_tracks)
        self.assertTrue(mock_print.call_count >= 2)
        mock_format.assert_not_called()

    @patch('music_player.library_search_scan.format_mm_ss')
    @patch('music_player.library_search_scan.print')
    def test_iteration_3_negated_element_constraint(self, mock_print, mock_format):
        mock_format.return_value = "05:00"
        s2_track = SimpleNamespace(title="Concolic Song", artist="Test Bot", duration_seconds=300)
        s1_tracks = [s2_track]
        _print_tracks_table(s1_tracks)
        call_args = mock_print.call_args[0][0]
        self.assertIn("Concolic Song", call_args)
        self.assertIn("Test Bot", call_args)
        self.assertIn("05:00", call_args)


if __name__ == '__main__':
    unittest.main()