import unittest
from unittest.mock import MagicMock, patch, mock_open
from music_player.player_metrics import load_data
from music_player.player_state import PlayerState


class TestConcolicExecution(unittest.TestCase):
    def setUp(self):
        self.mock_state = MagicMock(spec=PlayerState)
        self.mock_state.liked_tracks = set()

    @patch('music_player.player_metrics.DATA_FILE')
    def test_iter1_base_case(self, mock_data_file):
        s1 = None
        mock_data_file.exists.return_value = False  # S2 = False
        load_data(s1)
        mock_data_file.exists.assert_called()

    @patch('json.load')
    @patch('builtins.open', new_callable=mock_open)
    @patch('music_player.player_metrics.DATA_FILE')
    def test_iter2_derive_valid_execution(self, mock_data_file, mock_file_open, mock_json_load):
        s1 = self.mock_state
        mock_data_file.exists.return_value = True  # S2 = True
        data_payload = {"likes": ["track_A"], "counts": {}}
        mock_json_load.return_value = data_payload

        load_data(s1)
        self.assertIn("track_A", s1.liked_tracks)

    @patch('json.load')
    @patch('builtins.open', new_callable=mock_open)
    @patch('music_player.player_metrics.DATA_FILE')
    def test_iter3_derive_exception_path(self, mock_data_file, mock_file_open, mock_json_load):
        s1 = self.mock_state
        mock_data_file.exists.return_value = True  # S2 = True
        mock_json_load.side_effect = OSError("Disk Read Error")

        with patch('builtins.print') as mock_print:
            load_data(s1)
            mock_print.assert_called()
            args, _ = mock_print.call_args
            self.assertIn("Disk Read Error", args[0])


if __name__ == '__main__':
    unittest.main()