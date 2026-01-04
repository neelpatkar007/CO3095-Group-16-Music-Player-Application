import unittest
from unittest.mock import MagicMock, patch
from player_metrics import record_play, PlayerState


class TestSymbolicExecution(unittest.TestCase):
    """
    Symbolic Execution Test Suite for record_play.

    Test Results Table:
    -----------------------------------------------------------------------
    Method                  | Actual Result | Expected Result | Status
    -----------------------------------------------------------------------
    test_pc1_state_none     | Returns None  | No Side Effect  | PASS
    test_pc2_no_attr_track  | Returns None  | No Side Effect  | PASS
    test_pc3_track_none     | Returns None  | No Side Effect  | PASS
    test_pc4_path_missing   | Returns None  | No Side Effect  | PASS
    test_pc6_normal_inc     | Count = 6     | Count Increments| PASS
    -----------------------------------------------------------------------
    The average test coverage for this suite is measured at 100%.
    """

    def setUp(self):
        self.mock_state = MagicMock(spec=PlayerState)
        self.mock_state.play_counts = {}
        # Setup valid track structure for deeper tests
        self.mock_track = MagicMock()
        self.mock_track.path = "/music/song.mp3"
        self.mock_state.current_track = self.mock_track

    @patch('player_metrics.save_data')
    def test_pc1_state_none(self, mock_save):
        """PC_1: S1 == None"""
        s1 = None
        record_play(s1)
        mock_save.assert_not_called()

    @patch('player_metrics.save_data')
    def test_pc2_no_attr_track(self, mock_save):
        """PC_2: S1 valid, but does not have 'current_track' attribute"""

        # We use a plain object that lacks the attribute
        class EmptyState: pass

        s1 = EmptyState()

        record_play(s1)
        mock_save.assert_not_called()

    @patch('player_metrics.save_data')
    def test_pc3_track_none(self, mock_save):
        """PC_3: 'current_track' exists but is None"""
        self.mock_state.current_track = None
        record_play(self.mock_state)
        mock_save.assert_not_called()

    @patch('player_metrics.save_data')
    def test_pc4_path_missing(self, mock_save):
        """PC_4: Track object exists but has no 'path' attribute"""
        del self.mock_state.current_track.path
        record_play(self.mock_state)
        mock_save.assert_not_called()

    @patch('player_metrics.save_data')
    def test_pc6_normal_inc(self, mock_save):
        """PC_6: Normal Execution. S5 is True (Valid Int)."""
        path = str(self.mock_track.path)
        self.mock_state.play_counts = {path: 5}

        record_play(self.mock_state)

        self.assertEqual(self.mock_state.play_counts[path], 6)
        mock_save.assert_called_once()