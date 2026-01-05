import unittest
from unittest.mock import MagicMock, patch
import sys
from pathlib import Path

# Add the project root to sys.path
project_root = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(project_root))

from music_player.playlists_edit import add_track_from_library, _get_playlist


class TestConcolicExecution(unittest.TestCase):

    def setUp(self):
        self.state = MagicMock()
        self.state.tracks = [MagicMock()]
        self.playlist = MagicMock()
        self.playlist.tracks = None

    @patch('music_player.playlists_edit._get_playlist')
    def test_concolic_PC_6_invalid_int(self, mock_get_playlist):
        mock_get_playlist.return_value = (None, self.playlist)
        add_track_from_library(self.state, "sel", "not_an_int")
        self.assertEqual(len(self.playlist.tracks or []), 0)

    @patch('music_player.playlists_edit._get_playlist')
    def test_concolic_PC_7_out_of_bounds(self, mock_get_playlist):
        mock_get_playlist.return_value = (None, self.playlist)
        add_track_from_library(self.state, "sel", "99")

    @patch('music_player.playlists_edit._get_playlist')
    def test_concolic_PC_5_playlist_not_found(self, mock_get_playlist):
        mock_get_playlist.return_value = None
        result = add_track_from_library(self.state, "invalid_pl", "1")
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()