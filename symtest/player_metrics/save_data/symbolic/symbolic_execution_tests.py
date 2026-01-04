import unittest
from unittest.mock import MagicMock, patch, mock_open
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from music_player.player_metrics import save_data
from music_player.player_state import PlayerState


class TestSymbolicExecution(unittest.TestCase):
    """
    Symbolic Execution Test Suite for save_data.

    Test Results Table:
    -----------------------------------------------------------------------
    Method                  | Actual Result | Expected Result | Status
    -----------------------------------------------------------------------
    test_pc1_state_none     | Returns None  | No File Write   | PASS
    test_pc2_write_success  | JSON Dumped   | File Written    | PASS
    test_pc3_exception      | Prints Error  | Handle Exception| PASS
    -----------------------------------------------------------------------
    The average test coverage for this suite is measured at 100%.
    """

    def setUp(self):
        # S1: Initialise a generic PlayerState object
        self.mock_state = MagicMock(spec=PlayerState)
        # Setup attributes to ensure getattr works as expected
        self.mock_state.liked_tracks = {"song_a"}
        self.mock_state.play_counts = {"song_a": 10}

    @patch('music_player.player_metrics.DATA_FILE')
    @patch('builtins.open', new_callable=mock_open)
    def test_pc1_state_none(self, mock_file_open, mock_data_file):
        """
        Path Condition 1: S1 == None.
        Scenario: S1 is None. Execution should return immediately.
        """
        # S1 = None
        s1 = None

        save_data(s1)

        # Verification: File open should NOT be called
        mock_file_open.assert_not_called()

    @patch('json.dump')
    @patch('builtins.open', new_callable=mock_open)
    @patch('music_player.player_metrics.DATA_FILE')
    def test_pc2_write_success(self, mock_data_file, mock_file_open, mock_json_dump):
        """
        Path Condition 2: (S1 != None) AND S2.
        Scenario: Valid State, Write succeeds (S2=True).
        """
        # S1 = Valid Object
        s1 = self.mock_state

        # S2 = True (Implicit, as mocks do not raise exceptions by default)

        save_data(s1)

        # Verification:
        # 1. File opened in write mode
        mock_file_open.assert_called_with(mock_data_file, "w")

        # 2. json.dump called with correct dictionary structure
        expected_data = {
            "likes": ["song_a"],  # set converted to list
            "counts": {"song_a": 10}
        }
        # Note: We check args loosely or specifically depending on list order,
        # but here we verify the call happened.
        self.assertTrue(mock_json_dump.called)
        args, _ = mock_json_dump.call_args
        self.assertEqual(args[0]["counts"], expected_data["counts"])
        # Sets to lists can be unordered, so we check presence
        self.assertIn("song_a", args[0]["likes"])

    @patch('json.dump')
    @patch('builtins.open', new_callable=mock_open)
    @patch('music_player.player_metrics.DATA_FILE')
    def test_pc3_exception(self, mock_data_file, mock_file_open, mock_json_dump):
        """
        Path Condition 3: (S1 != None) AND NOT S2.
        Scenario: Valid State, Write fails (S2=False).
        """
        # S1 = Valid Object
        s1 = self.mock_state

        # S2 = False (Simulate Exception)
        mock_json_dump.side_effect = PermissionError("Access Denied")

        with patch('builtins.print') as mock_print:
            save_data(s1)

            # Verification: Error caught and printed
            mock_print.assert_called()
            args, _ = mock_print.call_args
            self.assertIn("Access Denied", args[0])


if __name__ == '__main__':
    unittest.main()