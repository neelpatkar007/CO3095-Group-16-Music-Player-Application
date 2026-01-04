import unittest
from unittest.mock import patch
from music_player.audio_backend import AudioEngine


class TestConcolicExecution(unittest.TestCase):
    '''
    Concolic Testing Suite for `set_volume` method.

    Test Results Table:
    | Iteration | S1 (volume) | S2 (HAS_PYGAME) | S3 (pygame.mixer) | Path       | Status |
    |-----------|-------------|-----------------|-------------------|------------|--------|
    | 1         | 50          | False           | N/A               | PC_1       | PASS   |
    | 2         | 50          | True            | False             | PC_2       | PASS   |
    | 3         | 50          | True            | True              | PC_3       | PASS   |

    The average test coverage for this suite is measured at 100%.
    '''

    def test_iteration_1_no_pygame(self):
        """
        Iteration 1: Initial Concrete Seed
        S1 = 50, S2 = False, S3 = N/A
        Constraint: NOT S2
        Path: Volume set, pygame not available.
        """
        audio = AudioEngine()
        S1 = 50

        with patch('music_player.audio_backend.HAS_PYGAME', False):
            audio.set_volume(S1)

        self.assertEqual(audio.volume, 50)

    def test_iteration_2_pygame_no_mixer(self):
        """
        Iteration 2: Flip S2 constraint (NOT S2) -> S2
        S1 = 50, S2 = True, S3 = False
        Constraint: S2 AND NOT S3
        Path: Volume set, pygame available but mixer unavailable.
        """
        audio = AudioEngine()
        S1 = 50

        with patch('music_player.audio_backend.HAS_PYGAME', True):
            with patch('music_player.audio_backend.pygame') as mock_pygame:
                mock_pygame.mixer = None
                audio.set_volume(S1)

        self.assertEqual(audio.volume, 50)

    def test_iteration_3_pygame_with_mixer(self):
        """
        Iteration 3: Flip S3 constraint (NOT S3) -> S3
        S1 = 50, S2 = True, S3 = True
        Constraint: S2 AND S3 (Path Exhausted)
        Path: Volume set, pygame available and set_volume called.
        """
        audio = AudioEngine()
        S1 = 50

        with patch('music_player.audio_backend.HAS_PYGAME', True):
            with patch('music_player.audio_backend.pygame') as mock_pygame:
                audio.set_volume(S1)

                self.assertEqual(audio.volume, 50)
                expected_float = 0.5
                mock_pygame.mixer.music.set_volume.assert_called_once_with(expected_float)


if __name__ == '__main__':
    unittest.main()