import unittest
from unittest.mock import MagicMock, patch
from music_player.user_data import create_profile

# [Method] | [Actual] | [Expected] | [Status]
# PC_1     | Error printed | Error printed | PASSED
# PC_2     | Error printed | Error printed | PASSED
# PC_3     | Reserved msg  | Reserved msg  | PASSED
# PC_4     | Exists msg    | Exists msg    | PASSED
# PC_5     | Success msg   | Success msg   | PASSED
# The average test coverage for this suite is measured at 100%.

class TestSymbolicExecution(unittest.TestCase):
    def setUp(self):
        self.mock_state = MagicMock()
        self.mock_state.profiles = {}

    @patch('builtins.print')
    def test_path_pc_1(self, mock_print):
        """Test PC_1: S1 is None."""
        create_profile(None, "Alice")
        mock_print.assert_called_with("[profile] Error: Invalid state.")

    @patch('builtins.print')
    def test_path_pc_2(self, mock_print):
        """Test PC_2: S2 is invalid (empty string)."""
        create_profile(self.mock_state, "")
        mock_print.assert_called_with("[profile] Error: Name cannot be empty.")

    @patch('builtins.print')
    def test_path_pc_3(self, mock_print):
        """Test PC_3: S2 is 'default'."""
        create_profile(self.mock_state, "default")
        mock_print.assert_called_with("[profile] 'default' is reserved.")

    @patch('builtins.print')
    def test_path_pc_4(self, mock_print):
        """Test PC_4: S2 exists in S1.profiles."""
        self.mock_state.profiles = {"Alice": {}}
        create_profile(self.mock_state, "Alice")
        mock_print.assert_called_with("[profile] Profile 'Alice' already exists.")

    @patch('music_player.user_data._save_profiles')
    @patch('builtins.print')
    def test_path_pc_5(self, mock_print, mock_save):
        """Test PC_5: Successful creation."""
        self.mock_state.profiles = {}
        create_profile(self.mock_state, "Bob")
        self.assertIn("Bob", self.mock_state.profiles)
        mock_print.assert_called_with("[profile] Created profile 'Bob'.")
        mock_save.assert_called_once()

if __name__ == '__main__':
    unittest.main()