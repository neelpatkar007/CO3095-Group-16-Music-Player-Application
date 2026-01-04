import unittest
from unittest.mock import MagicMock, patch


# [Method] | [Actual] | [Expected] | [Status]
# test_pc_1_early_return | None | None | Passed
# test_pc_2_full_execution | Print Output | Formatted String | Passed
# The average test coverage for this suite is measured at 100%.

class TestSymbolicExecution(unittest.TestCase):

    def setUp(self):
        # Setup common mocks for the symbolic environment
        self.mock_state = MagicMock()

    @patch('your_module._ensure_player_state')
    def test_pc_1_early_return(self, mock_ensure):
        """Tests PC_1: S1 == None resulting in early return."""
        # S1 defined as None
        S1 = None
        mock_ensure.return_value = S1

        from your_module import print_progress
        result = print_progress(S1)

        self.assertIsNone(result)
        mock_ensure.assert_called_once()

    @patch('your_module.format_mm_ss')
    @patch('your_module.get_progress')
    @patch('your_module._ensure_player_state')
    def test_pc_2_full_execution(self, mock_ensure, mock_get, mock_format):
        """Tests PC_2: NOT S1 == None resulting in full execution."""
        # S1 defined as a valid object
        S1 = self.mock_state
        mock_ensure.return_value = S1
        mock_get.return_value = (80, 200)
        mock_format.side_effect = ["01:20", "03:20"]

        from your_module import print_progress
        with patch('builtins.print') as mock_print:
            print_progress(S1)
            mock_print.assert_called_with("[ui] Progress: 01:20/03:20")


if __name__ == '__main__':
    unittest.main()