import unittest
from unittest.mock import Mock, patch
from music_player.user_data import list_profiles

class TestSymbolicExecution(unittest.TestCase):

    @patch('builtins.print')
    def test_pc1_null_state(self, mock_print):
        S1 = None
        list_profiles(S1)

    @patch('builtins.print')
    def test_pc2_active_match(self, mock_print):
        S1 = Mock()
        S1.profiles = {}
        S1.active_profile = "default"
        try:
            list_profiles(S1)
        except Exception as e:
            self.fail(f"PC_2 execution failed with {e}")

    @patch('builtins.print')
    def test_pc3_no_active_match(self, mock_print):
        """Path PC_3: S3 does not match any name in all_profiles."""
        S1 = Mock()
        S1.profiles = {"player1": {}}
        S1.active_profile = "none"
        try:
            list_profiles(S1)
        except Exception as e:
            self.fail(f"PC_3 execution failed with {e}")

if __name__ == '__main__':
    unittest.main()