import unittest
from unittest.mock import patch
from music_player.audio_backend import AudioEngine


class TestConcolicExecution(unittest.TestCase):


    def test_iteration_1_no_pygame(self):

        audio = AudioEngine()

        with patch('music_player.audio_backend.HAS_PYGAME', False):
            audio.stop()

    def test_iteration_2_with_pygame(self):

        audio = AudioEngine()

        with patch('music_player.audio_backend.HAS_PYGAME', True):
            with patch('music_player.audio_backend.pygame') as mock_pygame:
                audio.stop()


if __name__ == '__main__':
    unittest.main()