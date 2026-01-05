import unittest
from unittest.mock import MagicMock, patch
from music_player.player_metrics import record_play
from music_player.player_state import PlayerState

class TestConcolicExecution(unittest.TestCase):
    def setUp(self):
        self.mock_state = MagicMock(spec=PlayerState)
        self.mock_track = MagicMock()
        self.mock_track.path = "/music/song.mp3"
        self.mock_state.current_track = self.mock_track

    @patch('music_player.player_metrics.save_data')
    def test_iter_init_dict(self, mock_save):
        self.mock_state.play_counts = None
        record_play(self.mock_state)
        self.assertIsInstance(self.mock_state.play_counts, dict)
        self.assertEqual(self.mock_state.play_counts["/music/song.mp3"], 1)

    @patch('music_player.player_metrics.save_data')
    def test_iter_sanitize_str(self, mock_save):
        path = "/music/song.mp3"
        self.mock_state.play_counts = {path: "10"}
        record_play(self.mock_state)
        self.assertEqual(self.mock_state.play_counts[path], 1)

    @patch('music_player.player_metrics.save_data')
    def test_iter_sanitize_none(self, mock_save):
        path = "/music/song.mp3"
        self.mock_state.play_counts = {path: None}

        record_play(self.mock_state)

        self.assertEqual(self.mock_state.play_counts[path], 1)


if __name__ == '__main__':
    unittest.main()