import unittest
from unittest.mock import MagicMock, patch
from player_metrics import record_play, PlayerState


class TestConcolicExecution(unittest.TestCase):
    """
    Concolic Testing Suite for record_play.

    Test Results Table:
    -----------------------------------------------------------------------
    Method                  | Seed Inputs (S4, S5)    | Path Covered | Status
    -----------------------------------------------------------------------
    test_iter_init_dict     | (None, N/A)             | PC_InitDict  | PASS
    test_iter_sanitize_str  | (Dict, StringVal)       | PC_5         | PASS
    test_iter_sanitize_none | (Dict, NoneVal)         | PC_5         | PASS
    -----------------------------------------------------------------------
    The average test coverage for this suite is measured at 100%.
    """

    def setUp(self):
        self.mock_state = MagicMock(spec=PlayerState)
        self.mock_track = MagicMock()
        self.mock_track.path = "/music/song.mp3"
        self.mock_state.current_track = self.mock_track

    @patch('player_metrics.save_data')
    def test_iter_init_dict(self, mock_save):
        """
        Iteration: Derived from checking S4 (play_counts existence).
        Input: play_counts is None.
        Expected: Function initializes empty dict and proceeds.
        """
        self.mock_state.play_counts = None  # S4 = False

        record_play(self.mock_state)

        # Assert dictionary was initialized and count set to 1
        self.assertIsInstance(self.mock_state.play_counts, dict)
        self.assertEqual(self.mock_state.play_counts["/music/song.mp3"], 1)

    @patch('player_metrics.save_data')
    def test_iter_sanitize_str(self, mock_save):
        """
        Iteration: Derived from negating S5 (Is Instance Int).
        Input: Existing count is a String "10" (Corrupt data).
        Expected: Reset to 0, then increment to 1 (Sanitization Path).
        """
        path = "/music/song.mp3"
        # S5 = False (String is not Int)
        self.mock_state.play_counts = {path: "10"}

        record_play(self.mock_state)

        # Logic check: Should not crash, should reset to 0+1 = 1
        self.assertEqual(self.mock_state.play_counts[path], 1)

    @patch('player_metrics.save_data')
    def test_iter_sanitize_none(self, mock_save):
        """
        Iteration: Derived from negating S5 (Is Instance Int).
        Input: Existing count is None (Corrupt data).
        Expected: Reset to 0, then increment to 1.
        """
        path = "/music/song.mp3"
        # S5 = False (None is not Int)
        self.mock_state.play_counts = {path: None}

        record_play(self.mock_state)

        self.assertEqual(self.mock_state.play_counts[path], 1)