import unittest
from unittest.mock import MagicMock, patch
from music_player.player_metrics import toggle_like, save_data
from music_player.player_state import PlayerState


class TestSymbolicExecution(unittest.TestCase):
    def setUp(self):
        self.mock_state = MagicMock(spec=PlayerState)
        self.mock_state.liked_tracks = set()
        self.mock_state.current_track = MagicMock()
        self.mock_state.current_track.path = "/music/song.mp3"
        self.mock_state.current_track.display_name = "Song A"

    @patch('builtins.print')
    def test_pc1_state_none(self, mock_print):
        s1 = None
        toggle_like(s1)
        mock_print.assert_called_with("[metrics] Error: State is None.")

    @patch('builtins.print')
    def test_pc2_corrupt_data(self, mock_print):
        self.mock_state.liked_tracks = ["Not", "A", "Set"]
        toggle_like(self.mock_state)
        mock_print.assert_called_with("[metrics] Error: Liked tracks data corrupted.")

    @patch('builtins.print')
    def test_pc3_track_missing(self, mock_print):
        self.mock_state.current_track = None
        toggle_like(self.mock_state)
        mock_print.assert_called_with("[metrics] No track playing.")

    @patch('builtins.print')
    def test_pc4_path_invalid(self, mock_print):
        self.mock_state.current_track.path = "   "
        toggle_like(self.mock_state)
        mock_print.assert_called_with("[metrics] Error: Track path is empty.")

    @patch('music_player.player_metrics.save_data')
    @patch('builtins.print')
    def test_pc5_unlike_success(self, mock_print, mock_save):
        path = str(self.mock_state.current_track.path)
        self.mock_state.liked_tracks.add(path)
        toggle_like(self.mock_state)
        self.assertNotIn(path, self.mock_state.liked_tracks)
        mock_print.assert_called_with("[metrics] Unliked 'Song A'.")
        mock_save.assert_called_once()

    @patch('music_player.player_metrics.save_data')
    @patch('builtins.print')
    def test_pc7_like_success(self, mock_print, mock_save):
        toggle_like(self.mock_state)
        path = str(self.mock_state.current_track.path)
        self.assertIn(path, self.mock_state.liked_tracks)
        mock_print.assert_called_with("[metrics] Liked 'Song A'.")
        mock_save.assert_called_once()


if __name__ == '__main__':
    unittest.main()