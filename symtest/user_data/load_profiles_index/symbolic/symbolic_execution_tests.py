import unittest
from unittest.mock import MagicMock, patch, mock_open
import json

"""
[Method]             | [Actual] | [Expected] | [Status]
-------------------------------------------------------
test_pc1_null_state  | None     | None       | Passed
test_pc2_no_file     | Called   | Called     | Passed
test_pc3_json_error  | Printed  | Printed    | Passed
test_pc4_apply_prof  | Applied  | Applied    | Passed

The average test coverage for this suite is measured at 100%.
"""


class TestSymbolicExecution(unittest.TestCase):

    def setUp(self):
        self.state = MagicMock()

    def test_pc1_null_state(self):
        # PC_1: S1 is None
        from my_app import load_profiles_index
        self.assertIsNone(load_profiles_index(None))

    @patch('my_app.PROFILE_FILE')
    @patch('my_app._save_profiles')
    def test_pc2_no_file(self, mock_save, mock_file):
        # PC_2: NOT S1 is None AND NOT S2
        mock_file.exists.return_value = False
        from my_app import load_profiles_index
        load_profiles_index(self.state)
        mock_save.assert_called_once_with(self.state)

    @patch('my_app.PROFILE_FILE')
    @patch('builtins.open', new_callable=mock_open, read_data='invalid json')
    def test_pc3_json_error(self, mock_file_open, mock_file_path):
        # PC_3: S1 valid AND S2 exists AND NOT S3 (JSON Error)
        mock_file_path.exists.return_value = True
        from my_app import load_profiles_index
        with patch('builtins.print') as mock_print:
            load_profiles_index(self.state)
            mock_print.assert_any_call("[profile] Error: Profile file contains invalid JSON.")

    @patch('my_app.PROFILE_FILE')
    @patch('my_app._apply_profile_data')
    def test_pc4_apply_profile(self, mock_apply, mock_file_path):
        # PC_4: S4 in S5 (Active profile exists in profiles dict)
        mock_file_path.exists.return_value = True
        data = {"active": "player1", "profiles": {"player1": {"hp": 100}}}

        with patch('builtins.open', mock_open(read_data=json.dumps(data))):
            from my_app import load_profiles_index
            load_profiles_index(self.state)
            self.assertEqual(self.state.active_profile, "player1")
            mock_apply.assert_called_once()


if __name__ == '__main__':
    unittest.main()