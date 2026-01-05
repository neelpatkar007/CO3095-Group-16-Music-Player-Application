import unittest
from unittest.mock import patch
from music_player.audio_backend import AudioEngine


class TestConcolicStopReal(unittest.TestCase):


    def test_iteration_1_pygame_ok(self):

        audio = AudioEngine()

        with patch('music_player.audio_backend.pygame') as mock_pygame:
            audio._stop_real()

            mock_pygame.mixer.music.stop.assert_called_once()

    def test_iteration_2_no_pygame(self):

        audio = AudioEngine()

        with patch('music_player.audio_backend.pygame', None):
            with self.assertRaises(AssertionError):
                audio._stop_real()


if __name__ == '__main__':
    unittest.main()