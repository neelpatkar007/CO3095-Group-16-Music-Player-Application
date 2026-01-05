import unittest
from unittest.mock import MagicMock, patch
import sys
from pathlib import Path

# Add the project root to sys.path
project_root = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(project_root))

from music_player.playlists_edit import move_track_within_playlist



class TestConcolicTesting(unittest.TestCase):

    def setUp(self):
        self.mock_state = MagicMock()
        self.mock_track = MagicMock()
        self.mock_track.display_name = "TrackS7"
        self.mock_playlist = MagicMock()
        self.mock_playlist.tracks = [self.mock_track, MagicMock()]
        self.mock_playlist.name = "PlaylistName"

    @patch('music_player.playlists_edit._get_playlist')
    def test_PC6_from_out_bounds(self, mock_get):
        # Derived input: S3 is out of range of len(S6)
        mock_get.return_value = (None, self.mock_playlist)
        with patch('builtins.print') as mock_print:
            move_track_within_playlist(self.mock_state, "S2", "5", "1")
            mock_print.assert_called_with("[pl] 'from' index out of range.")

    @patch('music_player.playlists_edit._get_playlist')
    def test_PC7_to_out_bounds(self, mock_get):
        # Derived input: S4 is out of range
        mock_get.return_value = (None, self.mock_playlist)
        with patch('builtins.print') as mock_print:
            move_track_within_playlist(self.mock_state, "S2", "1", "10")
            mock_print.assert_called_with("[pl] 'to' index out of range.")

    @patch('music_player.playlists_edit._get_playlist')
    def test_PC10_successful_move(self, mock_get):
        mock_get.return_value = (None, self.mock_playlist)
        with patch('builtins.print') as mock_print:
            move_track_within_playlist(self.mock_state, "S2", "1", "2")
            mock_print.assert_any_call("[pl] Moved 'TrackS7' in playlist 'PlaylistName' from position 1 to 2.")

if __name__ == '__main__':
    unittest.main()