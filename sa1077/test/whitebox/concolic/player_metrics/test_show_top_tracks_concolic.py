import unittest
from unittest.mock import MagicMock, patch
from music_player.player_metrics import show_top_tracks
from music_player.player_state import PlayerState


class TestConcolicExecution(unittest.TestCase):
    def setUp(self):
        self.mock_state = MagicMock(spec=PlayerState)
        self.mock_state.library_tracks = []

    @patch('builtins.print')
    def test_iter_sanitize_data(self, mock_print):
        self.mock_state.play_counts = {
            "songA": 10,
            "songB": "20",
            "songC": None
        }
        show_top_tracks(self.mock_state)
        found_output = [call[0][0] for call in mock_print.call_args_list if "plays:" in call[0][0]]
        self.assertEqual(len(found_output), 1)
        self.assertIn("10 plays", found_output[0])

    @patch('builtins.print')
    def test_iter_filter_neg(self, mock_print):
        self.mock_state.play_counts = {"songA": 0, "songB": -1}
        show_top_tracks(self.mock_state)
        found_output = [call[0][0] for call in mock_print.call_args_list if "plays:" in call[0][0]]
        self.assertEqual(len(found_output), 0)

    @patch('builtins.print')
    def test_iter_limit_10(self, mock_print):
        self.mock_state.play_counts = {f"key{i}": 100 + i for i in range(11)}
        show_top_tracks(self.mock_state)
        found_output = [call[0][0] for call in mock_print.call_args_list if "plays:" in call[0][0]]
        self.assertEqual(len(found_output), 10)

    @patch('builtins.print')
    def test_iter_orphan_file(self, mock_print):
        path = "/missing/file.mp3"
        self.mock_state.play_counts = {path: 50}
        self.mock_state.library_tracks = []  # Empty lib
        show_top_tracks(self.mock_state)
        expected_msg = f"  50 plays: Unknown (File: {path})"
        mock_print.assert_any_call(expected_msg)


if __name__ == '__main__':
    unittest.main()