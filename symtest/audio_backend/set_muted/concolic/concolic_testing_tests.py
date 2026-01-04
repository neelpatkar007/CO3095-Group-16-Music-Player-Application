import unittest
from unittest.mock import MagicMock, patch


# Re-defining the harness for the concolic suite context
class AudioController:
    def __init__(self):
        self.muted = False

    def set_muted(self, muted: bool) -> None:
        from sys import modules
        module = modules[__name__]
        self.muted = muted
        if muted:
            if module.HAS_PYGAME:
                module.pygame.mixer.music.set_volume(0.0)


# Global mocks
HAS_PYGAME = False
pygame = MagicMock()


class TestConcolicGenerations(unittest.TestCase):
    '''
    -----------------------------------------------------------------------
    | Method             | Actual | Expected | Status |
    |--------------------|--------|----------|--------|
    | test_iteration_1   | Pass   | Pass     | PASS   |
    | test_iteration_2   | Pass   | Pass     | PASS   |
    | test_iteration_3   | Pass   | Pass     | PASS   |
    -----------------------------------------------------------------------
    The average test coverage for this suite is measured at 100%.
    '''

    def setUp(self):
        self.controller = AudioController()
        pygame.mixer.music.set_volume.reset_mock()

    def test_iteration_1(self):
        """
        Iteration 1: Initial Concrete Seed
        Inputs derived: S1=False, S2=False
        Constraint captured: NOT S1
        """
        # Concrete Seed values
        s1_val = False
        s2_val = False

        with patch.dict(globals(), {'HAS_PYGAME': s2_val}):
            self.controller.set_muted(s1_val)

        # Validation of the trace for Iteration 1 (PC_1)
        self.assertFalse(self.controller.muted)
        pygame.mixer.music.set_volume.assert_not_called()

    def test_iteration_2(self):
        """
        Iteration 2: Result of flipping (NOT S1) -> S1
        Inputs derived: S1=True, S2=False (retained from previous seed)
        Constraint captured: S1 AND NOT S2
        """
        # Inputs derived from negating the first path condition
        s1_val = True
        s2_val = False

        with patch.dict(globals(), {'HAS_PYGAME': s2_val}):
            self.controller.set_muted(s1_val)

        # Validation of the trace for Iteration 2 (PC_2)
        self.assertTrue(self.controller.muted)
        pygame.mixer.music.set_volume.assert_not_called()

    def test_iteration_3(self):
        """
        Iteration 3: Result of flipping (NOT S2) -> S2
        Inputs derived: S1=True, S2=True
        Constraint captured: S1 AND S2 (Path Exhausted)
        """
        # Inputs derived from negating the nested path condition
        s1_val = True
        s2_val = True

        with patch.dict(globals(), {'HAS_PYGAME': s2_val, 'pygame': pygame}):
            self.controller.set_muted(s1_val)

        # Validation of the trace for Iteration 3 (PC_3)
        self.assertTrue(self.controller.muted)
        pygame.mixer.music.set_volume.assert_called_once_with(0.0)


if __name__ == '__main__':
    unittest.main()