import unittest
from unittest.mock import patch
from music_player.audio_backend import AudioEngine

class TestConcolicExecution(unittest.TestCase):


    def test_iteration_1_no_pygame(self):

        audio = AudioEngine()
        S1 = 50

        with patch('music_player.audio_backend.HAS_PYGAME', False):
            audio.set_volume(S1)

        self.assertEqual(audio.volume, 50)

    def test_iteration_2_pygame_no_mixer(self):

        audio = AudioEngine()
        S1 = 50

        with patch('music_player.audio_backend.HAS_PYGAME', True):
            with patch('music_player.audio_backend.pygame') as mock_pygame:
                mock_pygame.mixer = None
                audio.set_volume(S1)

        self.assertEqual(audio.volume, 50)

    def test_iteration_3_pygame_with_mixer(self):

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