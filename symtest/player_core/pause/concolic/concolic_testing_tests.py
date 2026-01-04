import unittest
from unittest.mock import MagicMock
from music_player.player_core import pause
from music_player.player_state import PlayerState

class TestConcolicExecution(unittest.TestCase):
    """
    White-box testing suite based on Concolic Analysis (DART).

    Test Results Table:
    | Method               | Actual      | Expected    | Status |
    |----------------------|-------------|-------------|--------|
    | test_iter_1_pc_1     | No Action   | Early Ret   | PASS   |
    | test_iter_2_pc_2     | Paused      | Action Exec | PASS   |
    """

    def setUp(self):
        """Setup a reusable PlayerState with mocked audio engine and track."""
        self.mock_engine = MagicMock()
        self.mock_track = MagicMock()
        self.mock_track.path = "/dummy"
        self.mock_track.display_name = "Test Track"
        self.mock_track.duration_seconds = 300  # Optional

        self.state = PlayerState(tracks=[self.mock_track], audio_engine=self.mock_engine)
        self.state.position_seconds = 0
        self.state.playback_speed = 1.0

    def test_iter_1_pc_1(self):
        """
        Iteration 1: is_playing=False, is_paused=False
        Constraint: NOT S1 OR S2 -> hits guard clause (nothing to pause)
        """
        self.state.is_playing = False
        self.state.is_paused = False

        pause(self.state)

        # Verify pause() was not called
        self.mock_engine.pause.assert_not_called()
        self.assertFalse(self.state.is_playing)
        self.assertFalse(self.state.is_paused)

    def test_iter_2_pc_2(self):
        """
        Iteration 2: is_playing=True, is_paused=False
        Constraint: S1 AND NOT S2 -> hits action block (pause)
        """
        self.state.is_playing = True
        self.state.is_paused = False

        pause(self.state)

        # Verify pause() was called and flags updated
        self.mock_engine.pause.assert_called_once()
        self.assertFalse(self.state.is_playing)
        self.assertTrue(self.state.is_paused)


if __name__ == '__main__':
    unittest.main()
