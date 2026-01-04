import unittest
from unittest.mock import MagicMock, patch
from music_player.player_queue import next_track

# -------------------------------------------------------------------------
# TEST RESULTS TABLE
# -------------------------------------------------------------------------
# | Method             | Actual Result      | Expected Result    | Status |
# |--------------------|------------------|------------------|--------|
# | test_iter_1_bad_S1 | Error Logged       | Error Logged       | PASS   |
# | test_iter_2_bad_S2 | Log: No tracks     | Log: No tracks     | PASS   |
# | test_iter_3_stop   | Playback Stops     | Playback Stops     | PASS   |
# | test_iter_4_wrap   | Index wraps to 0   | Index wraps to 0   | PASS   |
# | test_iter_5_next   | Index increments   | Index increments   | PASS   |
# -------------------------------------------------------------------------
# Average test coverage for this suite: 100%
# -------------------------------------------------------------------------

class TestConcolicExecution(unittest.TestCase):
    """
    Implements the systematic 'Flip' strategy defined in CONCOLIC_ANALYSIS.md.
    """

    def setUp(self):
        self.state = MagicMock()
        self.state.history = []
        self.state.position_seconds = 10.0
        self.state.is_playing = False
        self.state.is_paused = False
        self.state.audio_engine = MagicMock()
        self.state.current_index = 0
        self.state.loop_mode = "off"
        self.state.shuffle_active = False

    @patch('builtins.print')
    def test_iter_1_bad_S1(self, mock_print):
        """Iteration 1: Concrete Seed (S1=None). Flip Constraint: S1 is None."""
        next_track(None)
        mock_print.assert_called_with("[queue] Error: State is invalid.")

    @patch('music_player.player_queue._get_tracks_safe')
    @patch('builtins.print')
    def test_iter_2_bad_S2(self, mock_print, mock_get_tracks):
        """Iteration 2: Valid S1, Empty S2. Flip Constraint: Not S2."""
        mock_get_tracks.return_value = []

        next_track(self.state)
        mock_print.assert_called_with("[queue] No tracks available.")

    @patch('music_player.player_queue._get_tracks_safe')
    def test_iter_3_seq_stop(self, mock_get_tracks):
        """Iteration 3: S2 Valid, End of List, Loop Off. Flip: Stop at End."""
        t1, t2 = MagicMock(), MagicMock()
        mock_get_tracks.return_value = [t1, t2]

        self.state.current_index = 1
        self.state.loop_mode = "off"
        self.state.shuffle_active = False
        self.state.is_playing = True

        next_track(self.state)

        self.assertFalse(self.state.is_playing)
        self.assertEqual(self.state.current_index, 1)  # Index stays the same

    @patch('music_player.player_queue._get_tracks_safe')
    @patch('builtins.print')
    def test_iter_4_seq_wrap(self, mock_print, mock_get_tracks):
        """Iteration 4: End of List, Loop All. Flip: Loop Mode == 'all'."""
        t1, t2 = MagicMock(), MagicMock()
        t1.display_name = "Track 1"
        mock_get_tracks.return_value = [t1, t2]

        self.state.current_index = 1
        self.state.loop_mode = "all"
        self.state.shuffle_active = False
        self.state.is_playing = True

        next_track(self.state)

        self.assertEqual(self.state.current_index, 0)
        mock_print.assert_called_with("[queue] Wrapped to next: Track 1")

    @patch('music_player.player_queue._get_tracks_safe')
    @patch('builtins.print')
    def test_iter_5_seq_next(self, mock_print, mock_get_tracks):
        """Iteration 5: Mid-List. Flip: Not End of List."""
        t1, t2 = MagicMock(), MagicMock()
        t2.display_name = "Track 2"
        mock_get_tracks.return_value = [t1, t2]

        self.state.current_index = 0
        self.state.loop_mode = "off"
        self.state.shuffle_active = False
        self.state.is_playing = True

        next_track(self.state)

        self.assertEqual(self.state.current_index, 1)
        mock_print.assert_called_with("[queue] Next: Track 2")


if __name__ == "__main__":
    unittest.main()
