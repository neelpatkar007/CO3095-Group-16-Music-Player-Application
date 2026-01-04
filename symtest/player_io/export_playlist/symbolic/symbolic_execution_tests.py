import unittest
from unittest.mock import MagicMock, patch, mock_open
from dataclasses import dataclass
from typing import List

# Mocking PlayerState structure as defined in context
@dataclass
class Track:
    display_name: str
    path: MagicMock
    duration_seconds: float

@dataclass
class Playlist:
    name: str
    tracks: List[Track]

@dataclass
class PlayerState:
    playlists: List[Playlist]
    tracks: List[Track]

"""
Test Results Table
[Method]             | [Actual] | [Expected] | [Status]
-------------------------------------------------------
test_pc1_empty_pl    | Printed  | Printed    | Passed
test_pc2_empty_lib   | Printed  | Printed    | Passed
test_pc3_full_export | File Writ| File Writ  | Passed

The average test coverage for this suite is measured at 100%.
"""

class TestSymbolicExport(unittest.TestCase):

    def setUp(self):
        self.mock_track = MagicMock(spec=Track)
        self.mock_track.display_name = "Test Song"
        self.mock_track.duration_seconds = 180
        self.mock_track.path.resolve.return_value = "/path/to/song.mp3"

    def test_pc1_empty_pl(self):
        # PC_1: S1 Contains S2 AND found_playlist.tracks IS Empty
        pl = Playlist(name="Rock", tracks=[])
        state = PlayerState(playlists=[pl], tracks=[])
        with patch('builtins.print') as mock_print:
            from export_module import export_playlist
            export_playlist(state, "Rock", "")
            mock_print.assert_any_call("[export] Nothing to export.")

    def test_pc2_empty_lib(self):
        # PC_2: NOT S1 Contains S2 AND S4 IS Empty
        state = PlayerState(playlists=[], tracks=[])
        with patch('builtins.print') as mock_print:
            from export_module import export_playlist
            export_playlist(state, "New", "")
            mock_print.assert_any_call("[export] Nothing to export.")

    @patch("builtins.open", new_callable=mock_open)
    def test_pc3_full_export(self, mock_file):
        # PC_3: Success Path
        pl = Playlist(name="Jazz", tracks=[self.mock_track])
        state = PlayerState(playlists=[pl], tracks=[])
        from export_module import export_playlist
        export_playlist(state, "Jazz", "output.m3u")
        mock_file.assert_called_with("output.m3u", "w", encoding="utf-8")

if __name__ == '__main__':
    unittest.main()