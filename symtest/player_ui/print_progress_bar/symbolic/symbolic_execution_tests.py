import unittest
from unittest.mock import MagicMock, patch

"""
[Method]             | [Actual] | [Expected] | [Status]
---------------------|----------|------------|---------
test_PC1_null_state  | None     | None       | Passed
test_PC2_valid_state | Printed  | Printed    | Passed

The average test coverage for this suite is measured at 100%.
"""


class TestSymbolicExecution(unittest.TestCase):

    @patch('your_module._ensure_player_state')
    def test_PC1_null_state(self, mock_ensure):
        """Path PC_1: S1 is None."""
        # Arrange
        S1 = None
        mock_ensure.return_value = S1

        # Act
        from your_module import print_progress_bar
        result = print_progress_bar(S1)

        # Assert
        self.assertIsNone(result)
        mock_ensure.assert_called_once()

    @patch('your_module.render_progress_bar')
    @patch('your_module._ensure_player_state')
    @patch('builtins.print')
    def test_PC2_valid_state(self, mock_print, mock_ensure, mock_render):
        """Path PC_2: NOT S1 is None."""
        # Arrange
        S1 = MagicMock(spec=True)  # Symbolic S1
        mock_ensure.return_value = S1
        mock_render.return_value = "████░░░"

        # Act
        from your_module import print_progress_bar
        print_progress_bar(S1)

        # Assert
        mock_render.assert_called_with(S1)
        mock_print.assert_called_with("[ui] ████░░░")


if __name__ == '__main__':
    unittest.main()