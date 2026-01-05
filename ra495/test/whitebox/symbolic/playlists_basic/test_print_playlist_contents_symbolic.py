import unittest
from unittest.mock import Mock, patch
import io
import sys
from music_player.playlists_basic import _print_playlist_contents


class TestSymbolicExecution(unittest.TestCase):

    def setUp(self):

        self.captured_output = io.StringIO()
        sys.stdout = self.captured_output

    def tearDown(self):
        sys.stdout = sys.__stdout__

    def test_pc1_empty_playlist(self):

        mock_playlist = Mock()
        mock_playlist.tracks = []

        _print_playlist_contents(mock_playlist)

        output = self.captured_output.getvalue().rstrip()
        self.assertEqual(output, "  (empty)", "PC_1 Failed: Did not print empty message.")

    @patch("music_player.playlists_basic.format_mm_ss")
    def test_pc2_populated_playlist(self, mock_format):

        mock_track = Mock()
        mock_track.duration_seconds = 180
        mock_track.display_name = "Symbolic Anthem"

        mock_playlist = Mock()
        mock_playlist.tracks = [mock_track]

        mock_format.return_value = "03:00"

        _print_playlist_contents(mock_playlist)

        output = self.captured_output.getvalue().rstrip()
        expected_output = "01. Symbolic Anthem [03:00]"

        self.assertEqual(output, expected_output, "PC_2 Failed: Output format incorrect.")
        mock_format.assert_called_once_with(180)


if __name__ == '__main__':
    unittest.main()
