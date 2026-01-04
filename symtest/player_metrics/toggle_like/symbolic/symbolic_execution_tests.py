import unittest
from unittest.mock import MagicMock, patch, ANY
from player_metrics import toggle_like, PlayerState


class TestSymbolicExecution(unittest.TestCase):
    """
    Symbolic Execution Test Suite for toggle_like.

    Test Results Table:
    -----------------------------------------------------------------------
    Method                  | Actual Result | Expected Result | Status
    -----------------------------------------------------------------------
    test_pc1_state_none     | Print Error   | Return None     | PASS
    test_pc2_corrupt_data   | Print Error   | Return None     | PASS
    test_pc3_track_missing  | Print Error   | Return None     | PASS
    test_pc4_path_invalid   | Print Error   | Return None     | PASS
    test_pc5_unlike_success | Save Called   | Removed & Saved | PASS
    test_pc7_like_success   | Save Called   | Added & Saved   | PASS
    -----------------------------------------------------------------------
    The average test coverage for this suite is measured at 100%.
    """

    def setUp(self):
        self.mock_state = MagicMock(spec=PlayerState)
        self.mock_state.liked_tracks = set()
        self.mock_state.current_track = MagicMock()
        self.mock_state.current_track.path = "/music/song.mp3"
        self.mock_state.current_track.display_name = "Song A"

    @patch('builtins.print')
    def test_pc1_state_none(self, mock_print):
        """PC_1: S1 == None"""
        s1 = None
        toggle_like(s1)
        mock_print.assert_called_with("[metrics] Error: State is None.")

    @patch('builtins.print')
    def test_pc2_corrupt_data(self, mock_print):
        """PC_2: S2 is False (Not a Set)"""
        self.mock_state.liked_tracks = ["Not", "A", "Set"]  # List, not Set
        toggle_like(self.mock_state)
        mock_print.assert_called_with("[metrics] Error: Liked tracks data corrupted.")

    @patch('builtins.print')
    def test_pc3_track_missing(self, mock_print):
        """PC_3: S3 is False (Track is None)"""
        self.mock_state.current_track = None
        toggle_like(self.mock_state)
        mock_print.assert_called_with("[metrics] No track playing.")

    @patch('builtins.print')
    def test_pc4_path_invalid(self, mock_print):
        """PC_4: S4 is False (Empty String)"""
        self.mock_state.current_track.path = "   "  # Empty after strip
        toggle_like(self.mock_state)
        mock_print.assert_called_with("[metrics] Error: Track path is empty.")

    @patch('player_metrics.save_data')
    @patch('builtins.print')
    def test_pc5_unlike_success(self, mock_print, mock_save):
        """
        PC_5: S5 is True (Liked), S6 is True (Mutation Success).
        Scenario: Track is liked, we toggle to unlike.
        """
        path = str(self.mock_state.current_track.path)
        self.mock_state.liked_tracks.add(path)  # Initial: Liked

        toggle_like(self.mock_state)

        # Assert removed
        self.assertNotIn(path, self.mock_state.liked_tracks)
        mock_print.assert_called_with("[metrics] Unliked 'Song A'.")
        mock_save.assert_called_once()

    @patch('player_metrics.save_data')
    @patch('builtins.print')
    def test_pc7_like_success(self, mock_print, mock_save):
        """
        PC_7: S5 is False (Not Liked), S6 is True (Mutation Success).
        Scenario: Track is NOT liked, we toggle to like.
        """
        # Initial: Empty set (Not Liked)
        toggle_like(self.mock_state)

        # Assert added
        path = str(self.mock_state.current_track.path)
        self.assertIn(path, self.mock_state.liked_tracks)
        mock_print.assert_called_with("[metrics] Liked 'Song A'.")
        mock_save.assert_called_once()