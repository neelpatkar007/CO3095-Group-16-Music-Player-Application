import unittest
from unittest.mock import MagicMock, patch
from music_player.player_metrics import record_play
from music_player.player_state import PlayerState


class TestSymbolicExecution(unittest.TestCase):
    def setUp(self):
        self.mock_state = MagicMock(spec=PlayerState)
        self.mock_state.play_counts = {}
        self.mock_track = MagicMock()
        self.mock_track.path = "/music/song.mp3"
        self.mock_state.current_track = self.mock_track

    @patch('music_player.player_metrics.save_data')
    def test_pc1_state_none(self, mock_save):
        s1 = None
        record_play(s1)
        mock_save.assert_not_called()

    @patch('music_player.player_metrics.save_data')
    def test_pc2_no_attr_track(self, mock_save):
        class EmptyState: pass
        s1 = EmptyState()
        record_play(s1)
        mock_save.assert_not_called()

    @patch('music_player.player_metrics.save_data')
    def test_pc3_track_none(self, mock_save):
        self.mock_state.current_track = None
        record_play(self.mock_state)
        mock_save.assert_not_called()

    @patch('music_player.player_metrics.save_data')
    def test_pc4_path_missing(self, mock_save):
        del self.mock_state.current_track.path
        record_play(self.mock_state)
        mock_save.assert_not_called()

    @patch('music_player.player_metrics.save_data')
    def test_pc6_normal_inc(self, mock_save):
        path = str(self.mock_track.path)
        self.mock_state.play_counts = {path: 5}
        record_play(self.mock_state)
        self.assertEqual(self.mock_state.play_counts[path], 6)
        mock_save.assert_called_once()


if __name__ == '__main__':
    unittest.main()