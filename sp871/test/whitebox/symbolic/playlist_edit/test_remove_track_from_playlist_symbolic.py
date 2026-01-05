import unittest
from unittest.mock import MagicMock, patch
import sys
from pathlib import Path


project_root = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(project_root))

from music_player.playlists_edit import remove_track_from_playlist


class TestSymbolicExecution(unittest.TestCase):

    def setUp(self):
        self.mock_state = MagicMock()
        self.mock_playlist = MagicMock()
        self.mock_track = MagicMock()
        self.mock_track.display_name = "Test Song"
        self.mock_playlist.name = "Test Playlist"
        self.mock_playlist.tracks = [self.mock_track]

    def test_pc1_none_state(self):
        # PC_1: S1 is None
        result = remove_track_from_playlist(None, "pop", "1")
        self.assertIsNone(result)

    def test_pc2_empty_selector(self):
        # PC_2: NOT S1 is None AND NOT S2
        result = remove_track_from_playlist(self.mock_state, "", "1")
        self.assertIsNone(result)

    def test_pc3_empty_index(self):
        # PC_3: S1 and S2 valid, but NOT S3
        result = remove_track_from_playlist(self.mock_state, "p1", "")
        self.assertIsNone(result)

    @patch('music_player.playlists_edit._get_playlist')
    def test_pc5_invalid_int(self, mock_get):
        # PC_5: S6 is Exception (non-integer string)
        mock_get.return_value = (None, self.mock_playlist)
        remove_track_from_playlist(self.mock_state, "p1", "not_a_number")
        # Analysis of printed output or side effect

    @patch('music_player.playlists_edit._get_playlist')
    def test_pc7_out_of_bounds(self, mock_get):
        # PC_7: NOT S6 < len S5 (Index too high)
        mock_get.return_value = (None, self.mock_playlist)
        remove_track_from_playlist(self.mock_state, "p1", "10")
        # Verify list size remains 1

    @patch('music_player.playlists_edit._get_playlist')
    def test_pc9_success(self, mock_get):
        # PC_9: All conditions satisfied
        mock_get.return_value = (None, self.mock_playlist)
        remove_track_from_playlist(self.mock_state, "p1", "1")
        self.assertEqual(len(self.mock_playlist.tracks), 0)

if __name__ == '__main__':
    unittest.main()