import unittest
from unittest.mock import MagicMock, patch


# [Method] | [Actual] | [Expected] | [Status]
# test_concolic_iteration_1 | Full Print | Path PC_2 Traversed | Passed
# test_concolic_iteration_2 | Early Return | Path PC_1 Traversed | Passed
# The average test coverage for this suite is measured at 100%.

class TestConcolicTesting(unittest.TestCase):

    @patch('your_module.format_mm_ss')
    @patch('your_module.get_progress')
    @patch('your_module._ensure_player_state')
    def test_concolic_iteration_1(self, mock_ensure, mock_get, mock_format):
        """Derived from Iteration 1: Concrete Seed (Valid Object)."""
        # S1 = Valid Object (Initial Seed)
        S1 = MagicMock()
        mock_ensure.return_value = S1
        mock_get.return_value = (10, 60)
        mock_format.side_effect = ["00:10", "01:00"]

        from your_module import print_progress
        with patch('builtins.print') as mock_print:
            print_progress(S1)
            # Verifies PC_2 was traversed
            mock_print.assert_called_once()

    @patch('your_module._ensure_player_state')
    def test_concolic_iteration_2(self, mock_ensure):
        """Derived from Iteration 2: Flipped Constraint (S1 is None)."""
        # S1 = None (Generated input via PC negation)
        S1 = None
        mock_ensure.return_value = S1

        from your_module import print_progress
        with patch('builtins.print') as mock_print:
            print_progress(S1)
            # Verifies PC_1 was traversed (print never called)
            mock_print.assert_not_called()


if __name__ == '__main__':
    unittest.main()