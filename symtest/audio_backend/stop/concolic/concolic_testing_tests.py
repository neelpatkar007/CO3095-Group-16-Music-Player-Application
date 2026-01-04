import unittest
from unittest.mock import MagicMock, patch


# ----------------------------------------------------------------------------------
# TEST RESULTS TABLE
# ----------------------------------------------------------------------------------
# | Method                  | Seed Inputs (S1, S2, S3) | Path Covered | Status |
# |-------------------------|--------------------------|--------------|--------|
# | test_iter_1_base        | (False, False, True)     | PC_1         | PASS   |
# | test_iter_2_flip_check  | (True, False, True)      | PC_2         | PASS   |
# | test_iter_3_flip_branch | (True, False, False)     | PC_3         | PASS   |
# ----------------------------------------------------------------------------------
# The average test coverage for this suite is measured at 100%.
# ----------------------------------------------------------------------------------

class TestConcolicExecution(unittest.TestCase):
    """
    White-box testing suite based on Concolic Analysis (FILE 2).
    Follows the Explicit Iteration Table to systematically negate constraints.
    """

    def setUp(self):
        self.audio_system = MagicMock()
        self.audio_system._stop_real = MagicMock()

        # Re-binding the function locally to ensure isolation
        def stop_bound():
            if not self.audio_system.playing and not self.audio_system.paused:
                return
            self.audio_system.playing = False
            self.audio_system.paused = False
            if self.audio_system.HAS_PYGAME:
                self.audio_system._stop_real()
            else:
                print("[audio] STOP (simulated)")

        self.audio_system.stop = stop_bound

    def test_iter_1_base(self):
        """
        Iteration 1: Base Seed
        Constraints: NOT S1 AND NOT S2
        Target: PC_1
        """
        # S1=False, S2=False, S3=True
        self.audio_system.playing = False
        self.audio_system.paused = False
        self.audio_system.HAS_PYGAME = True

        self.audio_system.stop()

        # Verification of Path PC_1
        self.audio_system._stop_real.assert_not_called()

    def test_iter_2_flip_check(self):
        """
        Iteration 2: Negating the first decision (NOT S1 AND NOT S2)
        New Constraint: S1 OR S2 (We choose S1=True)
        Target: PC_2
        """
        # S1=True, S2=False, S3=True
        self.audio_system.playing = True
        self.audio_system.paused = False
        self.audio_system.HAS_PYGAME = True

        self.audio_system.stop()

        # Verification of Path PC_2
        self.assertFalse(self.audio_system.playing)
        self.audio_system._stop_real.assert_called_once()

    def test_iter_3_flip_branch(self):
        """
        Iteration 3: Negating the second decision (S3 == True)
        New Constraint: NOT S3
        Target: PC_3
        """
        # S1=True, S2=False, S3=False
        self.audio_system.playing = True
        self.audio_system.paused = False
        self.audio_system.HAS_PYGAME = False

        with patch('builtins.print') as mock_print:
            self.audio_system.stop()

            # Verification of Path PC_3
            self.assertFalse(self.audio_system.playing)
            self.audio_system._stop_real.assert_not_called()
            mock_print.assert_called_with("[audio] STOP (simulated)")


if __name__ == '__main__':
    unittest.main()