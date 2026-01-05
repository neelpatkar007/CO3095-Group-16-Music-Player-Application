import unittest
from unittest.mock import MagicMock, patch, mock_open
import json

class TestSymbolicExecution(unittest.TestCase):

    def setUp(self):
        self.state = MagicMock()

    def test_pc1_null_state(self):
        from music_player.user_data import load_profiles_index
        self.assertIsNone(load_profiles_index(None))

    @patch('music_player.user_data.PROFILE_FILE')
    @patch('music_player.user_data._save_profiles')
    def test_pc2_no_file(self, mock_save, mock_file):
        mock_file.exists.return_value = False
        from music_player.user_data import load_profiles_index
        load_profiles_index(self.state)
        mock_save.assert_called_once_with(self.state)

    @patch('music_player.user_data.PROFILE_FILE')
    @patch('builtins.open', new_callable=mock_open, read_data='invalid json')
    def test_pc3_json_error(self, mock_file_open, mock_file_path):
        mock_file_path.exists.return_value = True
        from music_player.user_data import load_profiles_index
        with patch('builtins.print') as mock_print:
            load_profiles_index(self.state)
            mock_print.assert_any_call("[profile] Error: Profile file contains invalid JSON.")

    @patch('music_player.user_data.PROFILE_FILE')
    @patch('music_player.user_data._apply_profile_data')
    def test_pc4_apply_profile(self, mock_apply, mock_file_path):
        mock_file_path.exists.return_value = True
        data = {"active": "player1", "profiles": {"player1": {"hp": 100}}}

        with patch('builtins.open', mock_open(read_data=json.dumps(data))):
            from music_player.user_data import load_profiles_index
            load_profiles_index(self.state)
            self.assertEqual(self.state.active_profile, "player1")
            mock_apply.assert_called_once()


if __name__ == '__main__':
    unittest.main()