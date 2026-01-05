import unittest
from unittest.mock import patch
from music_player.audio_backend import AudioEngine


class TestSymbolicResumeReal(unittest.TestCase):

    def test_PC_1_assertion_fail(self):

        audio = AudioEngine()

        with patch('music_player.audio_backend.pygame', None):
            with self.assertRaises(AssertionError):
                audio._resume_real()

    def test_PC_2_nominal_execution(self):

        audio = AudioEngine()

        with patch('music_player.audio_backend.pygame') as mock_pygame:
            audio._resume_real()

            mock_pygame.mixer.music.unpause.assert_called_once()


if __name__ == '__main__':
    unittest.main()