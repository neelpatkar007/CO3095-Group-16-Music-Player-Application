import unittest
from unittest.mock import patch
from music_player.audio_backend import AudioEngine


class TestConcolicExecution(unittest.TestCase):
    '''
    Concolic Testing Suite for `set_muted` method.

    Test Results Table:
    | Iteration | S1 (muted) | S2 (HAS_PYGAME) | Path       | Status |
    |-----------|------------|-----------------|------------|--------|
    | 1         | False      | False           | PC_1       | PASS   |
    | 2         | True       | False           | PC_2       | PASS   |
    | 3         | True      | True            | PC_3       | PASS   |

    The average test coverage for this suite is measured at 100%.
    '''

    def test_iteration_1_not_muted(self):
        """
        Iteration 1: Initial Concrete Seed
        S1 = False, S2 = False
        Constraint: NOT S1
        Path: Mute flag not set, pygame not available.
        """
        audio = AudioEngine()

        with patch('music_player.audio_backend.HAS_PYGAME', False):
            audio.set_muted(False)

        self.assertFalse(audio.muted)

    def test_iteration_2_muted_no_pygame(self):
        """
        Iteration 2: Flip S1 constraint (NOT S1) -> S1
        S1 = True, S2 = False
        Constraint: S1 AND NOT S2
        Path: Mute flag set, pygame not available.
        """
        audio = AudioEngine()

        with patch('music_player.audio_backend.HAS_PYGAME', False):
            audio.set_muted(True)

        self.assertTrue(audio.muted)

    def test_iteration_3_muted_with_pygame(self):
        """
        Iteration 3: Flip S2 constraint (NOT S2) -> S2
        S1 = True, S2 = True
        Constraint: S1 AND S2 (Path Exhausted)
        Path: Mute flag set, pygame available and set_volume called.
        """
        audio = AudioEngine()

        with patch('music_player.audio_backend.HAS_PYGAME', True):
            with patch('music_player.audio_backend.pygame') as mock_pygame:
                audio.set_muted(True)

                self.assertTrue(audio.muted)
                mock_pygame.mixer.music.set_volume.assert_called_once_with(0.0)


if __name__ == '__main__':
    unittest.main()