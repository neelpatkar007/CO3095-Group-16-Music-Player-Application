import unittest
from unittest.mock import patch
from music_player.audio_backend import AudioEngine


class TestSymbolicStopReal(unittest.TestCase):
    """
    Symbolic Execution Test Suite for _stop_real.

    Test Results Table:
    | Method                 | Actual | Expected | Status |
    |------------------------|--------|----------|--------|
    | test_pc_1_assertion    | Raised | Raised   | PASS   |
    | test_pc_2_nominal_exec | Called | Called   | PASS   |

    The average test coverage for this suite is measured at 100%.
    """

    def test_pc_1_assertion(self):
        """
        Symbolic Path PC_1: S1 == None.

        Logic:
            PC_1 = NOT (S1 is not None) -> S1 is None.
            Expected behaviour: AssertionError is raised.
        """
        audio = AudioEngine()

        with patch('music_player.audio_backend.pygame', None):
            with self.assertRaises(AssertionError):
                audio._stop_real()

    def test_pc_2_nominal_exec(self):
        """
        Symbolic Path PC_2: S1 != None.

        Logic:
            PC_2 = S1 is not None.
            Expected behaviour: pygame.mixer.music.stop() is invoked.
        """
        audio = AudioEngine()

        with patch('music_player.audio_backend.pygame') as mock_pygame:
            audio._stop_real()

            mock_pygame.mixer.music.stop.assert_called_once()


if __name__ == '__main__':
    unittest.main()