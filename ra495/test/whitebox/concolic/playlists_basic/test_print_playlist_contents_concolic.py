import unittest
from unittest.mock import Mock, patch
import io
import sys
from music_player.playlists_basic import _print_playlist_contents


class TestConcolicExecution(unittest.TestCase):
    def setUp(self):
        self.captured_output = io.StringIO()
        sys.stdout = self.captured_output

    def tearDown(self):
        sys.stdout = sys.__stdout__

    def test_iteration_1_seed_empty(self):
        mock_playlist = Mock()
        mock_playlist.tracks = []

        _print_playlist_contents(mock_playlist)

        output = self.captured_output.getvalue().rstrip()
        self.assertEqual(output, "  (empty)", "Concolic Iteration 1 Failed.")

    @patch("music_player.playlists_basic.format_mm_ss")
    def test_iteration_2_seed_populated(self, mock_format):
        mock_track = Mock()
        mock_track.duration_seconds = 150
        mock_track.display_name = "Concrete Hit"

        mock_playlist = Mock()
        mock_playlist.tracks = [mock_track]

        mock_format.return_value = "02:30"

        _print_playlist_contents(mock_playlist)

        output = self.captured_output.getvalue().rstrip()
        expected_output = "01. Concrete Hit [02:30]"

        self.assertEqual(output, expected_output, "Concolic Iteration 2 Failed.")
        mock_format.assert_called_with(150)


if __name__ == '__main__':
    unittest.main()
