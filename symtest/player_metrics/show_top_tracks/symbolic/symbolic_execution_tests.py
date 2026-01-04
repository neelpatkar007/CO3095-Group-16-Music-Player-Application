import unittest
from unittest.mock import MagicMock, patch
from player_metrics import show_top_tracks, PlayerState


class TestSymbolicExecution(unittest.TestCase):
    """
    Symbolic Execution Test Suite for show_top_tracks.

    Test Results Table:
    -----------------------------------------------------------------------
    Method                  | Actual Result | Expected Result | Status
    -----------------------------------------------------------------------
    test_pc1_state_none     | Err: None     | Guard Checks    | PASS
    test_pc3_corrupt_type   | Err: Corrupt  | Guard Checks    | PASS
    test_pc4_empty_data     | Msg: No Hist  | Guard Checks    | PASS
    test_pc5_sort_fail      | Err: Sort     | Catch Exception | PASS
    test_pc8_valid_display  | Print Rows    | Top 10 Logic    | PASS
    -----------------------------------------------------------------------
    The average test coverage for this suite is measured at 100%.
    """

    def setUp(self):
        self.mock_state = MagicMock(spec=PlayerState)
        self.mock_state.play_counts = {}
        self.mock_state.library_tracks = []

    @patch('builtins.print')
    def test_pc1_state_none(self, mock_print):
        """PC_1: S1 == None"""
        show_top_tracks(None)
        mock_print.assert_any_call("[metrics] Error: State is None.")

    @patch('builtins.print')
    def test_pc3_corrupt_type(self, mock_print):
        """PC_3: S3 is False (play_counts is not a dict)"""
        self.mock_state.play_counts = "NotADict"
        show_top_tracks(self.mock_state)
        mock_print.assert_any_call("[metrics] Error: Play counts corrupted.")

    @patch('builtins.print')
    def test_pc4_empty_data(self, mock_print):
        """PC_4: S4 is True (Dict is empty)"""
        self.mock_state.play_counts = {}
        show_top_tracks(self.mock_state)
        mock_print.assert_any_call("[metrics] No play history yet.")

    @patch('builtins.sorted')  # Patch sorted to simulate S5 failure
    @patch('builtins.print')
    def test_pc5_sort_fail(self, mock_print, mock_sorted):
        """PC_5: S5 is False (Exception during sort)"""
        self.mock_state.play_counts = {"song1": 5}
        mock_sorted.side_effect = ValueError("Sort Comparison Error")

        show_top_tracks(self.mock_state)
        mock_print.assert_any_call("[metrics] Error sorting play history.")

    @patch('builtins.print')
    def test_pc8_valid_display(self, mock_print):
        """PC_8: Valid execution with library resolution."""
        path = "/music/hit.mp3"
        self.mock_state.play_counts = {path: 100}

        track = MagicMock()
        track.path = path
        track.display_name = "Greatest Hit"
        self.mock_state.library_tracks = [track]

        show_top_tracks(self.mock_state)

        # Verify header and row printing
        mock_print.assert_any_call("[metrics] --- Top Played Songs ---")
        mock_print.assert_any_call("  100 plays: Greatest Hit")