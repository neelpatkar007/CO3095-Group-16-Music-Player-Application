import unittest
from unittest.mock import MagicMock, patch
import sys
from pathlib import Path

# Add the project root to sys.path
project_root = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(project_root))

from music_player.playlists_edit import add_track_from_library



class TestSymbolicExecution(unittest.TestCase):

    def setUp(self):
        self.state = MagicMock()
        self.playlist = MagicMock()
        self.playlist.tracks = []
        self.track = MagicMock()
        self.track.display_name = "Song A"

    def test_PC_1_s1_none(self):
        # PC_1: S1 is None
        result = add_track_from_library(None, "selector", "1")
        self.assertIsNone(result)

    def test_PC_2_s2_empty(self):
        # PC_2: S1 valid, S2 (playlist_selector) is empty
        result = add_track_from_library(self.state, "", "1")
        self.assertIsNone(result)

    def test_PC_3_s3_empty(self):
        # PC_3: S1, S2 valid, S3 (library_index_str) is empty
        result = add_track_from_library(self.state, "selector", "")
        self.assertIsNone(result)

    @patch('music_player.playlists_edit._get_playlist')
    def test_PC_4_empty_lib(self, mock_get_playlist):
        # PC_4: S1.tracks is empty list
        self.state.tracks = []
        mock_get_playlist.return_value = (None, self.playlist)
        add_track_from_library(self.state, "sel", "1")
        # Function returns early after print

    @patch('music_player.playlists_edit._get_playlist')
    def test_PC_9_success(self, mock_get_playlist):
        # PC_9: Success path with display_name
        self.state.tracks = [self.track]
        mock_get_playlist.return_value = (None, self.playlist)
        add_track_from_library(self.state, "sel", "1")
        self.assertIn(self.track, self.playlist.tracks)

if __name__ == '__main__':
    unittest.main()