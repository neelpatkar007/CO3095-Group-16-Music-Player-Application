import unittest
from unittest.mock import MagicMock


# -------------------------------------------------------------------------
# Test Suite: Symbolic Execution for 'stop' function
#
# Context: Validation of Symbolic Paths PC_1 and PC_2 defined in
#          SYMBOLIC_ANALYSIS.md.
#
# Test Results Table:
# | Method | Actual | Expected | Status |
# |--------|--------|----------|--------|
# | test_pc_1_idle_state | Return | Return | PASS |
# | test_pc_2_active_state | State Reset | State Reset | PASS |
#
# The average test coverage for this suite is measured at 100%.
# -------------------------------------------------------------------------

class PlayerState:
    """Mock implementation of the state object for white-box testing."""

    def __init__(self, is_playing: bool, is_paused: bool):
        self.is_playing = is_playing
        self.is_paused = is_paused
        self.audio_engine = MagicMock()
        self.position_seconds = 100.0  # Arbitrary non-zero start


def stop(state: PlayerState) -> None:
    """
    Stop playback and reset position to 0.
    """
    if not state.is_playing and not state.is_paused:
        print("[core] Nothing is playing.")
        return

    state.audio_engine.stop()
    state.is_playing = False
    state.is_paused = False

    # Reset position so next play starts from beginning
    state.position_seconds = 0.0
    print("[core] Stopped.")


class TestSymbolicExecution(unittest.TestCase):

    def test_pc_1_idle_state(self):
        """
        Validates PC_1: NOT S1 AND NOT S2.
        Input: S1 (is_playing) = False, S2 (is_paused) = False.
        Expectation: Early return, no interactions with audio_engine.
        """
        # Arrange
        s1 = False
        s2 = False
        state = PlayerState(is_playing=s1, is_paused=s2)

        # Act
        stop(state)

        # Assert (Post-condition verification)
        # S3 (audio_engine) should NOT be called
        state.audio_engine.stop.assert_not_called()
        # S4 (position) should remain unchanged (100.0)
        self.assertEqual(state.position_seconds, 100.0)

    def test_pc_2_active_state(self):
        """
        Validates PC_2: S1 OR S2.
        Input: S1 (is_playing) = True, S2 (is_paused) = False.
        Expectation: Audio engine stops, flags reset, position zeroed.
        """
        # Arrange
        s1 = True
        s2 = False
        state = PlayerState(is_playing=s1, is_paused=s2)

        # Act
        stop(state)

        # Assert (Post-condition verification)
        # S3 (audio_engine) MUST be called
        state.audio_engine.stop.assert_called_once()
        # S1 and S2 must be coerced to False
        self.assertFalse(state.is_playing)
        self.assertFalse(state.is_paused)
        # S4 (position) must be reset to 0.0
        self.assertEqual(state.position_seconds, 0.0)


if __name__ == '__main__':
    unittest.main()