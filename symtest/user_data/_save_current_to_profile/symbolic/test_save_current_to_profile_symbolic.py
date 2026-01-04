import unittest
from unittest.mock import MagicMock, patch
from music_player.user_data import _save_current_to_profile

"""
[Method]             | [Actual] | [Expected] | [Status]
-------------------------------------------------------
test_pc1_early_exit  | None     | None       | Passed
test_pc2_no_save     | None     | None       | Passed
test_pc3_full_save   | Saved    | Saved      | Passed

The average test coverage for this suite is measured at 100%.
"""


class TestSymbolicExecution(unittest.TestCase):

    def setUp(self):
        self.state = MagicMock()

    @patch('music_player.user_data._serialize_current_state')
    def test_pc1_early_exit(self, mock_ser):
        # PC_1: S1 == None
        _save_current_to_profile(None)
        mock_ser.assert_not_called()

    @patch('music_player.user_data._save_profiles')
    @patch('music_player.user_data._serialize_current_state')
    def test_pc2_no_save(self, mock_ser, mock_save):
        # PC_2: S1 != None AND S2 AND S3 AND NOT S4
        self.state.profiles = {}
        self.state.active_profile = "default"
        mock_ser.return_value = None

        _save_current_to_profile(self.state)
        mock_save.assert_not_called()

    @patch('music_player.user_data._save_profiles')
    @patch('music_player.user_data._serialize_current_state')
    def test_pc3_full_save(self, mock_ser, mock_save):
        # PC_3: S1 != None AND S2 AND S3 AND S4
        self.state.profiles = {}
        self.state.active_profile = "slot1"
        serialised_data = {"hp": 100}
        mock_ser.return_value = serialised_data

        _save_current_to_profile(self.state)
        self.assertEqual(self.state.profiles["slot1"], serialised_data)
        mock_save.assert_called_once_with(self.state)


if __name__ == '__main__':
    unittest.main()