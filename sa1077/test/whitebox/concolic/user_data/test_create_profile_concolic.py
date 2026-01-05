import unittest
from unittest.mock import MagicMock, patch
from music_player.user_data import create_profile

class TestConcolicGeneration(unittest.TestCase):
    def setUp(self):
        self.state_s1 = MagicMock()
        self.state_s1.profiles = {}

    @patch('builtins.print')
    def test_iteration_1(self, mock_print):
        create_profile(None, "Alice")
        mock_print.assert_called_with("[profile] Error: Invalid state.")

    @patch('builtins.print')
    def test_iteration_2(self, mock_print):
        create_profile(self.state_s1, "")
        mock_print.assert_called_with("[profile] Error: Name cannot be empty.")

    @patch('builtins.print')
    def test_iteration_3(self, mock_print):
        create_profile(self.state_s1, "default")
        mock_print.assert_called_with("[profile] 'default' is reserved.")

    @patch('builtins.print')
    def test_iteration_4(self, mock_print):
        self.state_s1.profiles = {"Alice": {}}
        create_profile(self.state_s1, "Alice")
        mock_print.assert_any_call("[profile] Profile 'Alice' already exists.")

    @patch('music_player.user_data._save_profiles')
    @patch('builtins.print')
    def test_iteration_5(self, mock_print, mock_save):
        self.state_s1.profiles = {}
        create_profile(self.state_s1, "Bob")
        self.assertTrue("Bob" in self.state_s1.profiles)
        mock_save.assert_called_once()

if __name__ == '__main__':
    unittest.main()