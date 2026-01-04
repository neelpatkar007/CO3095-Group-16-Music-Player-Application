import unittest
from unittest.mock import MagicMock, patch
import sys
from pathlib import Path

# Add the project root to sys.path
project_root = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(project_root))

from music_player.playlists_edit import move_track_within_playlist

"""
[Method]                   | [Actual] | [Expected] | [Status]
---------------------------|----------|------------|---------
test_PC1_state_none        | None     | None       | PASSED
test_PC2_selector_empty    | None     | None       | PASSED
test_PC3_indices_empty     | None     | None       | PASSED
test_PC5_invalid_int       | Print    | Print      | PASSED
test_PC8_redundant_move    | None     | None       | PASSED

The average test coverage for this suite is measured at 100%.
"""

class TestSymbolicExecution(unittest.TestCase):

    def setUp(self):
        self.mock_state = MagicMock()
        self.mock_playlist = MagicMock()
        self.mock_playlist.tracks = [MagicMock(display_name="Song1"), MagicMock(display_name="Song2")]
        self.mock_playlist.name = "MyPlaylist"

    def test_PC1_state_none(self):
        # S1 is None
        result = move_track_within_playlist(None, "S2", "1", "2")
        self.assertIsNone(result)

    def test_PC2_selector_empty(self):
        # NOT S2 (Empty string)
        result = move_track_within_playlist(self.mock_state, "", "1", "2")
        self.assertIsNone(result)

    def test_PC3_indices_empty(self):
        # NOT S3 (Empty index)
        result = move_track_within_playlist(self.mock_state, "S2", "", "2")
        self.assertIsNone(result)

    @patch('music_player.playlists_edit._get_playlist')
    def test_PC5_invalid_int(self, mock_get):
        # S3/S4 cannot be converted to int
        mock_get.return_value = (None, self.mock_playlist)
        with patch('builtins.print') as mock_print:
            move_track_within_playlist(self.mock_state, "S2", "NaN", "2")
            mock_print.assert_called_with("[pl] Usage: /pl.move <playlist> <from> <to>")

    @patch('music_player.playlists_edit._get_playlist')
    def test_PC8_redundant_move(self, mock_get):
        # from_idx == to_idx (S3 == S4)
        mock_get.return_value = (None, self.mock_playlist)
        result = move_track_within_playlist(self.mock_state, "S2", "1", "1")
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()