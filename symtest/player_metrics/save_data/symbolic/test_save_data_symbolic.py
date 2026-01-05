import unittest
from unittest.mock import MagicMock, patch, mock_open
from music_player.player_metrics import save_data
from music_player.player_state import PlayerState


class TestSymbolicExecution(unittest.TestCase):
    def setUp(self):
        self.mock_state = MagicMock(spec=PlayerState)
        self.mock_state.liked_tracks = {"song_a"}
        self.mock_state.play_counts = {"song_a": 10}

    @patch('music_player.player_metrics.DATA_FILE')
    @patch('builtins.open', new_callable=mock_open)
    def test_pc1_state_none(self, mock_file_open, mock_data_file):
        s1 = None
        save_data(s1)
        mock_file_open.assert_not_called()

    @patch('json.dump')
    @patch('builtins.open', new_callable=mock_open)
    @patch('music_player.player_metrics.DATA_FILE')
    def test_pc2_write_success(self, mock_data_file, mock_file_open, mock_json_dump):
        s1 = self.mock_state
        save_data(s1)
        mock_file_open.assert_called_with(mock_data_file, "w")
        expected_data = {
            "likes": ["song_a"],  # set converted to list
            "counts": {"song_a": 10}
        }
        self.assertTrue(mock_json_dump.called)
        args, _ = mock_json_dump.call_args
        self.assertEqual(args[0]["counts"], expected_data["counts"])
        self.assertIn("song_a", args[0]["likes"])

    @patch('json.dump')
    @patch('builtins.open', new_callable=mock_open)
    @patch('music_player.player_metrics.DATA_FILE')
    def test_pc3_exception(self, mock_data_file, mock_file_open, mock_json_dump):
        s1 = self.mock_state
        mock_json_dump.side_effect = PermissionError("Access Denied")
        with patch('builtins.print') as mock_print:
            save_data(s1)
            mock_print.assert_called()
            args, _ = mock_print.call_args
            self.assertIn("Access Denied", args[0])


if __name__ == '__main__':
    unittest.main()