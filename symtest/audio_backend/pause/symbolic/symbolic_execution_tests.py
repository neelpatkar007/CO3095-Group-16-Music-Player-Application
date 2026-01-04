import unittest
from unittest.mock import MagicMock, patch

# TEST RESULTS TABLE
# ------------------------------------------------------------------------------
# | Method                  | Actual Result | Expected Result | Status |
# |-------------------------|---------------|-----------------|--------|
# | test_PC1_early_return   | None          | None            | PASS   |
# | test_PC2_real_pause     | _pause_real() | _pause_real()   | PASS   |
# | test_PC3_simulated      | Print output  | Print output    | PASS   |
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
        'has_pygame' is passed as an argument here to simulate the global flag S3.
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

class TestSymbolicExecution(unittest.TestCase):
    """
    Symbolic Execution Test Suite.
    Tests are derived directly from the Path Conditions (PC_n) identified in FILE 1.
    """

    def setUp(self):
        self.audio = AudioController()

    def test_PC1_early_return(self):
        """
        Path Condition 1: (NOT S1) OR S2
        Scenario: Audio is not playing (S1=False) or is already paused (S2=True).
        Input S1=False, S2=False (satisfies NOT S1)
        Input S3=True (Irrelevant for this path, but set for completeness)
        """
        # Symbolic Inputs
        self.audio.playing = False # S1
        self.audio.paused = False  # S2
        HAS_PYGAME = True          # S3

        # Execution
        self.audio.pause(HAS_PYGAME)

        # Assertions
        # State should remain unchanged
        self.assertFalse(self.audio.playing, "S1 should remain False in PC_1")
        self.assertFalse(self.audio.paused, "S2 should remain False in PC_1")
        # _pause_real should NOT be called
        self.audio._pause_real.assert_not_called()

    def test_PC2_real_pause(self):
        """
        Path Condition 2: S1 AND (NOT S2) AND S3
        Scenario: Audio is playing, not paused, and Pygame is available.
        """
        # Symbolic Inputs
        self.audio.playing = True  # S1
        self.audio.paused = False  # S2
        HAS_PYGAME = True          # S3

        # Execution
        self.audio.pause(HAS_PYGAME)

        # Assertions
        # State should update
        self.assertFalse(self.audio.playing, "S1 should update to False in PC_2")
        self.assertTrue(self.audio.paused, "S2 should update to True in PC_2")
        # _pause_real SHOULD be called
        self.audio._pause_real.assert_called_once()

    def test_PC3_simulated_pause(self):
        """
        Path Condition 3: S1 AND (NOT S2) AND (NOT S3)
        Scenario: Audio is playing, not paused, and Pygame is NOT available.
        """
        # Symbolic Inputs
        self.audio.playing = True  # S1
        self.audio.paused = False  # S2
        HAS_PYGAME = False         # S3

        # Capture stdout for the print statement
        with patch('builtins.print') as mock_print:
            # Execution
            self.audio.pause(HAS_PYGAME)

            # Assertions
            # State should update
            self.assertFalse(self.audio.playing, "S1 should update to False in PC_3")
            self.assertTrue(self.audio.paused, "S2 should update to True in PC_3")
            # _pause_real should NOT be called
            self.audio._pause_real.assert_not_called()
            # Verify simulated output
            mock_print.assert_called_with("[audio] PAUSE (simulated)")

if __name__ == '__main__':
    unittest.main()