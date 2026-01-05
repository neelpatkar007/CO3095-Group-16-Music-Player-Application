import unittest
from unittest.mock import MagicMock, patch, mock_open
import json

class TestConcolicExecution(unittest.TestCase):

    def setUp(self):
        self.state = MagicMock()

    @patch('music_player.user_data.PROFILE_FILE')
    def test_iter1_flip_s1(self, mock_file):
        from music_player.user_data import load_profiles_index
        mock_file.exists.return_value = False
        load_profiles_index(self.state)

    @patch('music_player.user_data.PROFILE_FILE')
    @patch('music_player.user_data._save_current_to_profile')
    def test_iter4_default_save(self, mock_save_default, mock_file_path):
        from music_player.user_data import load_profiles_index
        mock_file_path.exists.return_value = True
        data = {"active": "default", "profiles": {}}

        with patch('builtins.open', mock_open(read_data=json.dumps(data))):
            load_profiles_index(self.state)
            self.assertEqual(self.state.active_profile, "default")
            mock_save_default.assert_called_once_with(self.state)

    @patch('music_player.user_data.PROFILE_FILE')
    def test_non_dict_data(self, mock_file_path):
        from music_player.user_data import load_profiles_index
        mock_file_path.exists.return_value = True
        data = ["not", "a", "dict"]

        with patch('builtins.open', mock_open(read_data=json.dumps(data))):
            load_profiles_index(self.state)
            self.assertEqual(self.state.active_profile, "default")
            self.assertIn("default", self.state.profiles)


if __name__ == '__main__':
    unittest.main()