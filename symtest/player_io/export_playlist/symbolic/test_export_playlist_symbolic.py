import unittest
from unittest.mock import MagicMock, patch, mock_open
from dataclasses import dataclass
from typing import List
from pathlib import Path

from music_player.player_io import export_playlist
from music_player.player_state import PlayerState

@dataclass
class Track:
    display_name: str
    path: Path
    duration_seconds: float

@dataclass
class Playlist:
    name: str
    tracks: List[Track]

class TestSymbolicExport(unittest.TestCase):

    def setUp(self):
        self.mock_track = MagicMock()
        self.mock_track.display_name = "Test Song"
        self.mock_track.duration_seconds = 180
        self.mock_track.path = MagicMock()
        self.mock_track.path.resolve.return_value = "/path/to/song.mp3"

    def test_pc1_empty_pl(self):
        pl = MagicMock()
        pl.name = "Rock"
        pl.tracks = []

        state = MagicMock(spec=PlayerState)
        state.playlists = [pl]
        state.tracks = []

        with patch('builtins.print') as mock_print:
            export_playlist(state, "Rock", "")
            mock_print.assert_any_call("[export] Nothing to export.")

    def test_pc2_empty_lib(self):
        state = MagicMock(spec=PlayerState)
        state.playlists = []
        state.tracks = []

        with patch('builtins.print') as mock_print:
            export_playlist(state, "New", "")
            mock_print.assert_any_call("[export] Nothing to export.")

    @patch("builtins.open", new_callable=mock_open)
    def test_pc3_full_export(self, mock_file):
        pl = MagicMock()
        pl.name = "Jazz"
        pl.tracks = [self.mock_track]

        state = MagicMock(spec=PlayerState)
        state.playlists = [pl]
        state.tracks = []

        export_playlist(state, "Jazz", "output.m3u")
        mock_file.assert_called_with("output.m3u", "w", encoding="utf-8")


if __name__ == '__main__':
    unittest.main()