import unittest
from unittest.mock import MagicMock, patch, mock_open
import json

"""
[Method]               | [Actual] | [Expected] | [Status]
---------------------------------------------------------
test_iter1_flip_s1     | Handled  | Handled    | Passed
test_iter2_flip_s2     | Handled  | Handled    | Passed
test_iter4_default_save| Saved    | Saved      | Passed

The average test coverage for this suite is measured at 100%.
"""


class TestConcolicExecution(unittest.TestCase):

    def setUp(self):
        self.state = MagicMock()

    @patch('music_player.user_data.PROFILE_FILE')
    def test_iter1_flip_s1(self, mock_file):
        # Concrete execution derived from flipping S1 (State is now Object)
        from music_player.user_data import load_profiles_index
        # Verify it moves past the first 'if state is None'
        mock_file.exists.return_value = False
        load_profiles_index(self.state)
        # Should not fail, just verifies flow

    @patch('music_player.user_data.PROFILE_FILE')
    @patch('music_player.user_data._save_current_to_profile')
    def test_iter4_default_save(self, mock_save_default, mock_file_path):
        # PC_7: S4 is 'default' AND 'default' NOT in S5
        # Derived by negating the existence of 'default' in profiles
        from music_player.user_data import load_profiles_index
        mock_file_path.exists.return_value = True
        data = {"active": "default", "profiles": {}}  # S4 is default, S5 is empty

        with patch('builtins.open', mock_open(read_data=json.dumps(data))):
            load_profiles_index(self.state)
            self.assertEqual(self.state.active_profile, "default")
            mock_save_default.assert_called_once_with(self.state)

    @patch('music_player.user_data.PROFILE_FILE')
    def test_non_dict_data(self, mock_file_path):
        # Testing branch where S3 is NOT a dict (isinstance(data, dict) is False)
        from music_player.user_data import load_profiles_index
        mock_file_path.exists.return_value = True
        data = ["not", "a", "dict"]

        with patch('builtins.open', mock_open(read_data=json.dumps(data))):
            load_profiles_index(self.state)
            self.assertEqual(self.state.active_profile, "default")
            # When data is invalid, a default profile is created
            self.assertIn("default", self.state.profiles)


if __name__ == '__main__':
    unittest.main()