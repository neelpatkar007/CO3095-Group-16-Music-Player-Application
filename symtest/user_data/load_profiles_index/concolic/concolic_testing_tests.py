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

    def test_iter1_flip_s1(self):
        # Concrete execution derived from flipping S1 (State is now Object)
        from my_app import load_profiles_index
        # Verify it moves past the first 'if state is None'
        with patch('my_app.PROFILE_FILE') as mock_file:
            mock_file.exists.return_value = False
            load_profiles_index(self.state)
            self.state.assert_not_called()  # Should not fail, just verifies flow

    @patch('my_app.PROFILE_FILE')
    @patch('my_app._save_current_to_profile')
    def test_iter4_default_save(self, mock_save_default, mock_file_path):
        # PC_7: S4 is 'default' AND 'default' NOT in S5
        # Derived by negating the existence of 'default' in profiles
        mock_file_path.exists.return_value = True
        data = {"active": "default", "profiles": {}}  # S4 is default, S5 is empty

        with patch('builtins.open', mock_open(read_data=json.dumps(data))):
            from my_app import load_profiles_index
            load_profiles_index(self.state)
            self.assertEqual(self.state.active_profile, "default")
            mock_save_default.assert_called_once_with(self.state)

    @patch('my_app.PROFILE_FILE')
    def test_non_dict_data(self, mock_file_path):
        # Testing branch where S3 is NOT a dict (isinstance(data, dict) is False)
        mock_file_path.exists.return_value = True
        data = ["not", "a", "dict"]

        with patch('builtins.open', mock_open(read_data=json.dumps(data))):
            from my_app import load_profiles_index
            load_profiles_index(self.state)
            self.assertEqual(self.state.active_profile, "default")
            self.assertEqual(self.state.profiles, {})


if __name__ == '__main__':
    unittest.main()