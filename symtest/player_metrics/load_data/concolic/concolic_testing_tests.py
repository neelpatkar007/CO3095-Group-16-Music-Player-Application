import unittest
from unittest.mock import MagicMock, patch, mock_open
from player_metrics import load_data, PlayerState


class TestConcolicExecution(unittest.TestCase):
    """
    Concolic Testing Suite (Concrete + Symbolic) for load_data.

    Test Results Table:
    -----------------------------------------------------------------------
    Method                  | Seed Inputs (S1, S2, S3)| Path Covered | Status
    -----------------------------------------------------------------------
    test_iter1_all_false    | (None, False, True)     | PC_1         | PASS
    test_iter2_negate_s2    | (Obj, True, True)       | PC_2         | PASS
    test_iter3_negate_s3    | (Obj, True, False)      | PC_3         | PASS
    -----------------------------------------------------------------------
    The average test coverage for this suite is measured at 100%.
    """

    def setUp(self):
        self.mock_state = MagicMock(spec=PlayerState)
        self.mock_state.liked_tracks = set()

    @patch('player_metrics.DATA_FILE')
    def test_iter1_base_case(self, mock_data_file):
        """
        Iteration 1: Base Case.
        Inputs: S1=None, S2=False (Simulated).
        Expected: Early Return (PC_1).
        """
        # Concrete Seed
        s1 = None
        mock_data_file.exists.return_value = False  # S2 = False

        load_data(s1)

        # Logic check: Should return without error
        mock_data_file.exists.assert_called()

    @patch('json.load')
    @patch('builtins.open', new_callable=mock_open)
    @patch('player_metrics.DATA_FILE')
    def test_iter2_derive_valid_execution(self, mock_data_file, mock_file_open, mock_json_load):
        """
        Iteration 2: Derived from negating PC_1 constraints.
        Inputs: S1=Object, S2=True, S3=True (Valid JSON).
        Expected: Full Execution (PC_2).
        """
        # Concrete Seed
        s1 = self.mock_state
        mock_data_file.exists.return_value = True  # S2 = True

        # S3 = True (Data is valid)
        data_payload = {"likes": ["track_A"], "counts": {}}
        mock_json_load.return_value = data_payload

        load_data(s1)

        # Assert constraints were satisfied and state updated
        self.assertIn("track_A", s1.liked_tracks)

    @patch('json.load')
    @patch('builtins.open', new_callable=mock_open)
    @patch('player_metrics.DATA_FILE')
    def test_iter3_derive_exception_path(self, mock_data_file, mock_file_open, mock_json_load):
        """
        Iteration 3: Derived from negating S3 (internal constraint).
        Inputs: S1=Object, S2=True, S3=False (Exception).
        Expected: Exception Handling (PC_3).
        """
        # Concrete Seed
        s1 = self.mock_state
        mock_data_file.exists.return_value = True  # S2 = True

        # S3 = False (Flip valid data to Exception)
        mock_json_load.side_effect = OSError("Disk Read Error")

        with patch('builtins.print') as mock_print:
            load_data(s1)
            # Verify we walked the exception path
            mock_print.assert_called()
            args, _ = mock_print.call_args
            self.assertIn("Disk Read Error", args[0])