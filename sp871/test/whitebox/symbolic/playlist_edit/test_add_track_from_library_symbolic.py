import unittest
from unittest.mock import MagicMock, patch
import sys
from pathlib import Path


from music_player.playlists_edit import add_track_from_library



class TestSymbolicExecution(unittest.TestCase):

    def setUp(self):
        self.state = MagicMock()
        self.playlist = MagicMock()
        self.playlist.tracks = []
        self.track = MagicMock()
        self.track.display_name = "Song A"

    def test_PC_1_s1_none(self):
        result = add_track_from_library(None, "selector", "1")
        self.assertIsNone(result)

    def test_PC_2_s2_empty(self):
        result = add_track_from_library(self.state, "", "1")
        self.assertIsNone(result)

    def test_PC_3_s3_empty(self):
        result = add_track_from_library(self.state, "selector", "")
        self.assertIsNone(result)

    @patch('music_player.playlists_edit._get_playlist')
    def test_PC_4_empty_lib(self, mock_get_playlist):
        self.state.tracks = []
        mock_get_playlist.return_value = (None, self.playlist)
        add_track_from_library(self.state, "sel", "1")

    @patch('music_player.playlists_edit._get_playlist')
    def test_PC_9_success(self, mock_get_playlist):
        self.state.tracks = [self.track]
        mock_get_playlist.return_value = (None, self.playlist)
        add_track_from_library(self.state, "sel", "1")
        self.assertIn(self.track, self.playlist.tracks)

if __name__ == '__main__':
    unittest.main()