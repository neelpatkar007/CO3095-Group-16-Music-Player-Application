import unittest
from unittest.mock import MagicMock, patch, mock_open
from music_player.player_metrics import load_data
from music_player.player_state import PlayerState


class TestSymbolicExecution(unittest.TestCase):
    def setUp(self):
        self.mock_state = MagicMock(spec=PlayerState)
        self.mock_state.liked_tracks = set()
        self.mock_state.play_counts = {}

    @patch('music_player.player_metrics.DATA_FILE')
    def test_pc1_state_none(self, mock_data_file):
        s1 = None
        mock_data_file.exists.return_value = True
        load_data(s1)
        mock_data_file.exists.assert_called()

    @patch('music_player.player_metrics.DATA_FILE')
    def test_pc1_file_missing(self, mock_data_file):
        s1 = self.mock_state
        mock_data_file.exists.return_value = False
        load_data(s1)
        self.assertFalse(hasattr(s1, 'mock_open_called'))

    @patch('json.load')
    @patch('builtins.open', new_callable=mock_open)
    @patch('music_player.player_metrics.DATA_FILE')
    def test_pc2_load_success(self, mock_data_file, mock_file_open, mock_json_load):
        s1 = self.mock_state
        mock_data_file.exists.return_value = True
        mock_json_load.return_value = {"likes": ["song1.mp3"], "counts": {"song1.mp3": 5}}
        load_data(s1)
        self.assertEqual(s1.liked_tracks, {"song1.mp3"})
        self.assertEqual(s1.play_counts, {"song1.mp3": 5})

    @patch('json.load')
    @patch('builtins.open', new_callable=mock_open)
    @patch('music_player.player_metrics.DATA_FILE')
    def test_pc3_exception(self, mock_data_file, mock_file_open, mock_json_load):
        s1 = self.mock_state
        mock_data_file.exists.return_value = True
        mock_json_load.side_effect = ValueError("Corrupt JSON")

        with patch('builtins.print') as mock_print:
            load_data(s1)
            mock_print.assert_called_with("[metrics] Error loading data: Corrupt JSON")

        self.assertEqual(s1.liked_tracks, set())


if __name__ == '__main__':
    unittest.main()