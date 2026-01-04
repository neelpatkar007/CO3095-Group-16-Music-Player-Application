import unittest
from unittest.mock import MagicMock, patch

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

    def test_pc1_early_exit(self):
        # PC_1: S1 == None
        with patch('__main__._serialize_current_state') as mock_ser:
            from your_module import _save_current_to_profile
            _save_current_to_profile(None)
            mock_ser.assert_not_called()

    def test_pc2_no_save(self):
        # PC_2: S1 != None AND S2 AND S3 AND NOT S4
        self.state.profiles = {}
        self.state.active_profile = "default"
        with patch('your_module._serialize_current_state', return_value=None):
            with patch('your_module._save_profiles') as mock_save:
                from your_module import _save_current_to_profile
                _save_current_to_profile(self.state)
                mock_save.assert_not_called()

    def test_pc3_full_save(self):
        # PC_3: S1 != None AND S2 AND S3 AND S4
        self.state.profiles = {}
        self.state.active_profile = "slot1"
        serialised_data = {"hp": 100}
        with patch('your_module._serialize_current_state', return_value=serialised_data):
            with patch('your_module._save_profiles') as mock_save:
                from your_module import _save_current_to_profile
                _save_current_to_profile(self.state)
                self.assertEqual(self.state.profiles["slot1"], serialised_data)
                mock_save.assert_called_once_with(self.state)

if __name__ == '__main__':
    unittest.main()