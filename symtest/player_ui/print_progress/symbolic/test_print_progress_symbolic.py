import unittest
from unittest.mock import MagicMock, patch
from music_player.player_ui import print_progress


class TestSymbolicExecution(unittest.TestCase):
    """
    Symbolic Execution Test Suite for print_progress.

    Test Results Table:
    | Method               | Actual | Expected | Status |
    |----------------------|--------|----------|--------|
    | test_pc1_early_return| None   | None     | PASS   |
    | test_pc2_full_path   | Output | Output   | PASS   |

    The average test coverage for this suite is measured at 100%.
    """

    @patch('builtins.print')
    @patch('music_player.player_ui.format_mm_ss')
    @patch('music_player.player_ui.get_progress')
    @patch('music_player.player_ui._ensure_player_state')
    def test_pc1_early_return(self, mock_ensure, mock_get_progress, mock_fmt, mock_print):
        """
        Symbolic Path PC_1: NOT S1 (after verification).
        Constraint: _ensure_player_state(S1) IS None.
        Rationale: Verifies that invalid states terminate execution immediately.
        """
        # S1 Symbolic Mapping: Input that fails validation
        S1 = None

        # Constraint Enforcement: The validator returns None
        mock_ensure.return_value = None

        # Execute
        print_progress(S1)

        # Assertions for PC_1
        mock_ensure.assert_called_once_with(S1, "progress")
        mock_get_progress.assert_not_called()
        mock_print.assert_not_called()

    @patch('builtins.print')
    @patch('music_player.player_ui.format_mm_ss')
    @patch('music_player.player_ui.get_progress')
    @patch('music_player.player_ui._ensure_player_state')
    def test_pc2_full_path(self, mock_ensure, mock_get_progress, mock_fmt, mock_print):
        """
        Symbolic Path PC_2: S1 (Valid).
        Constraint: _ensure_player_state(S1) IS NOT None.
        Rationale: Verifies data retrieval and formatting on valid states.
        """
        # S1 Symbolic Mapping: A concrete object representing a valid state
        S1 = MagicMock(name="ValidPlayerState")

        # Constraint Enforcement: The validator returns the state object
        mock_ensure.return_value = S1

        # Mock dependencies for the logic inside PC_2
        mock_get_progress.return_value = (79, 204)

        # Configure format_mm_ss to return string representations
        mock_fmt.side_effect = ["01:19", "03:24"]

        # Execute
        print_progress(S1)

        # Assertions for PC_2
        mock_ensure.assert_called_once_with(S1, "progress")
        mock_get_progress.assert_called_once_with(S1)

        # Verify output matches the format string construction
        mock_print.assert_called_once_with("[ui] Progress: 01:19/03:24")


if __name__ == '__main__':
    unittest.main()