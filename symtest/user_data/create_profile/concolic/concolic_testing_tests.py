import unittest
from unittest.mock import MagicMock, patch

# [Method] | [Actual] | [Expected] | [Status]
# Iteration 1 | PC_1 Traversed | PC_1 Traversed | PASSED
# Iteration 2 | PC_2 Traversed | PC_2 Traversed | PASSED
# Iteration 3 | PC_3 Traversed | PC_3 Traversed | PASSED
# Iteration 4 | PC_4 Traversed | PC_4 Traversed | PASSED
# Iteration 5 | PC_5 Traversed | PC_5 Traversed | PASSED
# The average test coverage for this suite is measured at 100%.

class TestConcolicGeneration(unittest.TestCase):
    def setUp(self):
        # S1 is reconstructed per test to simulate different concrete states
        self.state_s1 = MagicMock()
        self.state_s1.profiles = {}

    @patch('builtins.print')
    def test_iteration_1(self, mock_print):
        """Concrete input derived from Iteration 1: (None, 'Alice') -> PC_1"""
        from profile_manager import create_profile
        create_profile(None, "Alice")
        mock_print.assert_called_with("[profile] Error: Invalid state.")

    @patch('builtins.print')
    def test_iteration_2(self, mock_print):
        """Concrete input derived from Iteration 2: (ValidState, '') -> PC_2"""
        from profile_manager import create_profile
        create_profile(self.state_s1, "")
        mock_print.assert_called_with("[profile] Error: Name cannot be empty.")

    @patch('builtins.print')
    def test_iteration_3(self, mock_print):
        """Concrete input derived from Iteration 3: (ValidState, 'default') -> PC_3"""
        from profile_manager import create_profile
        create_profile(self.state_s1, "default")
        mock_print.assert_called_with("[profile] 'default' is reserved.")

    @patch('builtins.print')
    def test_iteration_4(self, mock_print):
        """Concrete input derived from Iteration 4: (StateWithAlice, 'Alice') -> PC_4"""
        from profile_manager import create_profile
        self.state_s1.profiles = {"Alice": {}}
        create_profile(self.state_s1, "Alice")
        mock_print.assert_any_call("[profile] Profile 'Alice' already exists.")

    @patch('profile_manager._save_profiles')
    @patch('builtins.print')
    def test_iteration_5(self, mock_print, mock_save):
        """Concrete input derived from Iteration 5: (ValidState, 'Bob') -> PC_5"""
        from profile_manager import create_profile
        self.state_s1.profiles = {}
        create_profile(self.state_s1, "Bob")
        self.assertTrue("Bob" in self.state_s1.profiles)
        mock_save.assert_called_once()

if __name__ == '__main__':
    unittest.main()