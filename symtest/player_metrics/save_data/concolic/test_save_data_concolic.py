import unittest
from unittest.mock import MagicMock, patch, mock_open
from music_player.player_metrics import save_data
from music_player.player_state import PlayerState


class TestConcolicExecution(unittest.TestCase):
    def setUp(self):
        self.mock_state = MagicMock(spec=PlayerState)
        self.mock_state.liked_tracks = set()
        self.mock_state.play_counts = {}

    @patch('builtins.open', new_callable=mock_open)
    def test_iter1_base_case(self, mock_file_open):
        s1 = None
        save_data(s1)
        mock_file_open.assert_not_called()

    @patch('json.dump')
    @patch('builtins.open', new_callable=mock_open)
    def test_iter2_derive_valid_execution(self, mock_file_open, mock_json_dump):
        s1 = self.mock_state
        save_data(s1)
        mock_file_open.assert_called()
        mock_json_dump.assert_called()

    @patch('json.dump')
    @patch('builtins.open', new_callable=mock_open)
    def test_iter3_derive_exception_path(self, mock_file_open, mock_json_dump):
        s1 = self.mock_state
        mock_json_dump.side_effect = TypeError("Object not serializable")

        with patch('builtins.print') as mock_print:
            save_data(s1)
            mock_print.assert_called()
            args, _ = mock_print.call_args
            self.assertIn("Object not serializable", args[0])


if __name__ == '__main__':
    unittest.main()