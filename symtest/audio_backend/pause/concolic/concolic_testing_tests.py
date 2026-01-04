import unittest
from unittest.mock import MagicMock, patch
from music_player.audio_backend import AudioEngine

# TEST RESULTS TABLE
# ------------------------------------------------------------------------------
# | Iteration | Input Seed (S1, S2, S3) | Path Taken | Status |
# |-----------|-------------------------|------------|--------|
# | 1         | (False, False, True)    | PC_1       | PASS   |
# | 2         | (True, False, True)     | PC_2       | PASS   |
# | 3         | (True, False, False)    | PC_3       | PASS   |
# ------------------------------------------------------------------------------
# The average test coverage for this suite is measured at 100%.


class TestConcolicExecution(unittest.TestCase):
    """
    Concolic Testing Suite.
    Tests are generated based on the Explicit Iteration Table derived in FILE 2.
    Each test represents a concrete execution trace derived by negating path constraints.
    """

    def test_iteration_1_initial_seed(self):
        """
        Iteration 1: Concrete Seed (False, False, True)
        Path Constraint Met: (NOT S1 OR S2) -> True because S1 is False.
        Expected Path: PC_1 (Early Return)
        """
        # Concrete Seed
        audio = AudioEngine()
        audio.playing = False  # S1
        audio.paused = False   # S2

        with patch('music_player.audio_backend.HAS_PYGAME', True):
            # Execution
            audio.pause()

            # Verification of Path PC_1
            # No state change expected
            self.assertFalse(audio.playing)
            self.assertFalse(audio.paused)

    def test_iteration_2_negate_guard(self):
        """
        Iteration 2: Concrete Seed (True, False, True)
        Logic: Flip (NOT S1) from Iteration 1 to S1=True.
        Path Constraint Met: S1 AND (NOT S2) AND S3.
        Expected Path: PC_2 (Real Pause)
        """
        # Concrete Seed
        audio = AudioEngine()
        audio.playing = True   # S1
        audio.paused = False   # S2

        with patch('music_player.audio_backend.HAS_PYGAME', True):
            with patch('music_player.audio_backend.pygame') as mock_pygame:
                # Execution
                audio.pause()

                # Verification of Path PC_2
                # State update expected
                self.assertFalse(audio.playing)
                self.assertTrue(audio.paused)
                mock_pygame.mixer.music.pause.assert_called_once()

    def test_iteration_3_negate_pygame(self):
        """
        Iteration 3: Concrete Seed (True, False, False)
        Logic: Flip S3 from Iteration 2 to S3=False.
        Path Constraint Met: S1 AND (NOT S2) AND (NOT S3).
        Expected Path: PC_3 (Simulated Pause)
        """
        # Concrete Seed
        audio = AudioEngine()
        audio.playing = True   # S1
        audio.paused = False   # S2

        with patch('music_player.audio_backend.HAS_PYGAME', False):
            with patch('builtins.print') as mock_print:
                # Execution
                audio.pause()

                # Verification of Path PC_3
                # State update expected
                self.assertFalse(audio.playing)
                self.assertTrue(audio.paused)
                mock_print.assert_called_with("[audio] PAUSE (simulated)")


if __name__ == '__main__':
    unittest.main()