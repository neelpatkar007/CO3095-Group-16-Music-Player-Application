import unittest
from unittest.mock import patch
from music_player.audio_backend import AudioEngine


class TestConcolicExecution(unittest.TestCase):

    def test_iteration_1_not_muted(self):

        audio = AudioEngine()

        with patch('music_player.audio_backend.HAS_PYGAME', False):
            audio.set_muted(False)

        self.assertFalse(audio.muted)

    def test_iteration_2_muted_no_pygame(self):

        audio = AudioEngine()

        with patch('music_player.audio_backend.HAS_PYGAME', False):
            audio.set_muted(True)

        self.assertTrue(audio.muted)

    def test_iteration_3_muted_with_pygame(self):

        audio = AudioEngine()

        with patch('music_player.audio_backend.HAS_PYGAME', True):
            with patch('music_player.audio_backend.pygame') as mock_pygame:
                audio.set_muted(True)

                self.assertTrue(audio.muted)
                mock_pygame.mixer.music.set_volume.assert_called_once_with(0.0)


if __name__ == '__main__':
    unittest.main()