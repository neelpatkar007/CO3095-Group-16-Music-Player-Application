import unittest
from unittest.mock import patch
from music_player.audio_backend import AudioEngine


class TestConcolicResumeReal(unittest.TestCase):

    def test_iteration_1_seed_none(self):

        audio = AudioEngine()

        with patch('music_player.audio_backend.pygame', None):
            with self.assertRaises(AssertionError):
                audio._resume_real()

    def test_iteration_2_seed_mock(self):

        audio = AudioEngine()

        with patch('music_player.audio_backend.pygame') as mock_pygame:
            audio._resume_real()

            mock_pygame.mixer.music.unpause.assert_called_once()


if __name__ == '__main__':
    unittest.main()