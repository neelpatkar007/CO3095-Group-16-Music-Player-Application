import unittest
from unittest.mock import MagicMock, patch
import sys
from pathlib import Path

project_root = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(project_root))

from music_player.playlists_edit import remove_track_from_playlist, _get_playlist


class TestConcolicTesting(unittest.TestCase):

    def test_iteration_1_pc1(self):
        # Concrete Seed (None, "", "") -> PC_1
        remove_track_from_playlist(None, "", "")

    def test_iteration_2_pc2(self):
        # Concrete Seed (State, "", "") -> PC_2
        state = MagicMock()
        remove_track_from_playlist(state, "", "")

    def test_iteration_3_pc3(self):
        # Concrete Seed (State, "p1", "") -> PC_3
        state = MagicMock()
        remove_track_from_playlist(state, "p1", "")

    @patch('music_player.playlists_edit._get_playlist')
    def test_iteration_4_pc5(self, mock_get):
        # Concrete Seed (State, "p1", "abc") -> PC_5
        state = MagicMock()
        pl = MagicMock()
        mock_get.return_value = (None, pl)
        remove_track_from_playlist(state, "p1", "abc")

    @patch('music_player.playlists_edit._get_playlist')
    def test_iteration_5_pc7(self, mock_get):
        # Concrete Seed (State, "p1", "0") -> PC_7 (Since 0-1 = -1)
        state = MagicMock()
        pl = MagicMock()
        pl.tracks = []
        mock_get.return_value = (None, pl)
        remove_track_from_playlist(state, "p1", "0")

    @patch('music_player.playlists_edit._get_playlist')
    def test_iteration_6_pc9(self, mock_get):
        # Concrete Seed (State, "p1", "1") -> PC_9
        state = MagicMock()
        pl = MagicMock()
        track = MagicMock()
        track.display_name = "Song"
        pl.tracks = [track]
        pl.name = "My List"
        mock_get.return_value = (None, pl)
        remove_track_from_playlist(state, "p1", "1")
        self.assertEqual(len(pl.tracks), 0)

if __name__ == '__main__':
    unittest.main()