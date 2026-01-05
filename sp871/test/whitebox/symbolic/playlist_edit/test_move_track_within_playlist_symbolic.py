import unittest
from unittest.mock import MagicMock, patch
import sys
from pathlib import Path


project_root = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(project_root))

from music_player.playlists_edit import move_track_within_playlist



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
        result = move_track_within_playlist(self.mock_state, "", "1", "2")
        self.assertIsNone(result)

    def test_PC3_indices_empty(self):
        result = move_track_within_playlist(self.mock_state, "S2", "", "2")
        self.assertIsNone(result)

    @patch('music_player.playlists_edit._get_playlist')
    def test_PC5_invalid_int(self, mock_get):
        mock_get.return_value = (None, self.mock_playlist)
        with patch('builtins.print') as mock_print:
            move_track_within_playlist(self.mock_state, "S2", "NaN", "2")
            mock_print.assert_called_with("[pl] Usage: /pl.move <playlist> <from> <to>")

    @patch('music_player.playlists_edit._get_playlist')
    def test_PC8_redundant_move(self, mock_get):
        mock_get.return_value = (None, self.mock_playlist)
        result = move_track_within_playlist(self.mock_state, "S2", "1", "1")
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()