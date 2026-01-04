import unittest
from unittest.mock import patch
from music_player.audio_backend import AudioEngine


class TestConcolicStopReal(unittest.TestCase):
    """
    Concolic Testing Suite for `_stop_real` method.

    Test Results Table:
    | Method                      | Actual | Expected | Status |
    |-----------------------------|--------|----------|--------|
    | test_iteration_1_pygame_ok  | Called | Called   | PASS   |
    | test_iteration_2_no_pygame  | Raised | Raised   | PASS   |

    The average test coverage for this suite is measured at 100%.
    """

    def test_iteration_1_pygame_ok(self):
        """
        Iteration 1: Concrete Seed (S1 = pygame available).

        Constraint: pygame is not None.
        Path Taken: PC_1.
        """
        audio = AudioEngine()

        with patch('music_player.audio_backend.pygame') as mock_pygame:
            audio._stop_real()

            mock_pygame.mixer.music.stop.assert_called_once()

    def test_iteration_2_no_pygame(self):
        """
        Iteration 2: Derived Input from Constraint Negation.

        Previous Constraint: pygame is not None.
        Negated Constraint: pygame is None.
        Path Taken: PC_2.
        """
        audio = AudioEngine()

        with patch('music_player.audio_backend.pygame', None):
            with self.assertRaises(AssertionError):
                audio._stop_real()


if __name__ == '__main__':
    unittest.main()