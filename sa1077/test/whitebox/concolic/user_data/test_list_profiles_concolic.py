import unittest
from unittest.mock import Mock, patch
from music_player.user_data import list_profiles

class TestConcolicExecution(unittest.TestCase):

    @patch('builtins.print')
    def test_iteration_1_negation(self, mock_print):
        S1 = None
        list_profiles(S1)

    @patch('builtins.print')
    def test_iteration_2_flip(self, mock_print):
        S1 = Mock()
        S1.profiles = {}
        S1.active_profile = "default"
        try:
            list_profiles(S1)
        except Exception as e:
            self.fail(f"Concolic Iteration 2 failed: {e}")

    @patch('builtins.print')
    def test_iteration_3_terminal(self, mock_print):
        S1 = Mock()
        S1.profiles = {"pro_user": {}}
        S1.active_profile = "default"
        try:
            list_profiles(S1)
        except Exception as e:
            self.fail(f"Concolic Iteration 3 failed: {e}")

if __name__ == '__main__':
    unittest.main()