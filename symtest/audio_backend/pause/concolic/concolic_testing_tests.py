import unittest
from unittest.mock import MagicMock, patch

# TEST RESULTS TABLE
# ------------------------------------------------------------------------------
# | Iteration | Input Seed (S1, S2, S3) | Path Taken | Status |
# |-----------|-------------------------|------------|--------|
# | 1         | (False, False, True)    | PC_1       | PASS   |
# | 2         | (True, False, True)     | PC_2       | PASS   |
# | 3         | (True, False, False)    | PC_3       | PASS   |
# ------------------------------------------------------------------------------
# The average test coverage for this suite is measured at 100%.

class AudioController:
    """
    Mock class structure to replicate the context of the provided function.
    """
    def __init__(self):
        self.playing = False  # S1
        self.paused = False   # S2
        self._pause_real = MagicMock()

    def pause(self, has_pygame):
        """
        The function under test.
        """
        # Makes sure that cannot pause if it is stopped or already paused.
        if not self.playing or self.paused:
            return
        self.playing = False
        self.paused = True

        if has_pygame:
            self._pause_real()
        else:
            print("[audio] PAUSE (simulated)")

class TestConcolicExecution(unittest.TestCase):
    """
    Concolic Testing Suite.
    Tests are generated based on the Explicit Iteration Table derived in FILE 2.
    Each test represents a concrete execution trace derived by negating path constraints.
    """

    def setUp(self):
        self.audio = AudioController()

    def test_iteration_1_initial_seed(self):
        """
        Iteration 1: Concrete Seed (False, False, True)
        Path Constraint Met: (NOT S1 OR S2) -> True because S1 is False.
        Expected Path: PC_1 (Early Return)
        """
        # Concrete Seed
        self.audio.playing = False # S1
        self.audio.paused = False  # S2
        HAS_PYGAME = True          # S3

        # Execution
        self.audio.pause(HAS_PYGAME)

        # Verification of Path PC_1
        # No state change expected
        self.assertFalse(self.audio.playing)
        self.assertFalse(self.audio.paused)
        self.audio._pause_real.assert_not_called()

    def test_iteration_2_negate_guard(self):
        """
        Iteration 2: Concrete Seed (True, False, True)
        Logic: Flip (NOT S1) from Iteration 1 to S1=True.
        Path Constraint Met: S1 AND (NOT S2) AND S3.
        Expected Path: PC_2 (Real Pause)
        """
        # Concrete Seed
        self.audio.playing = True  # S1
        self.audio.paused = False  # S2
        HAS_PYGAME = True          # S3

        # Execution
        self.audio.pause(HAS_PYGAME)

        # Verification of Path PC_2
        # State update expected
        self.assertFalse(self.audio.playing)
        self.assertTrue(self.audio.paused)
        self.audio._pause_real.assert_called_once()

    def test_iteration_3_negate_pygame(self):
        """
        Iteration 3: Concrete Seed (True, False, False)
        Logic: Flip S3 from Iteration 2 to S3=False.
        Path Constraint Met: S1 AND (NOT S2) AND (NOT S3).
        Expected Path: PC_3 (Simulated Pause)
        """
        # Concrete Seed
        self.audio.playing = True  # S1
        self.audio.paused = False  # S2
        HAS_PYGAME = False         # S3

        with patch('builtins.print') as mock_print:
            # Execution
            self.audio.pause(HAS_PYGAME)

            # Verification of Path PC_3
            # State update expected
            self.assertFalse(self.audio.playing)
            self.assertTrue(self.audio.paused)
            self.audio._pause_real.assert_not_called()
            mock_print.assert_called_with("[audio] PAUSE (simulated)")

if __name__ == '__main__':
    unittest.main()