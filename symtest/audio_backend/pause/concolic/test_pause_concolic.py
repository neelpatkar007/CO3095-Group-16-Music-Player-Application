import unittest
from unittest.mock import MagicMock, patch
from music_player.audio_backend import AudioEngine

class TestConcolicExecution(unittest.TestCase):

    def test_iteration_1_initial_seed(self):

        audio = AudioEngine()
        audio.playing = False
        audio.paused = False

        with patch('music_player.audio_backend.HAS_PYGAME', True):

            audio.pause()


            self.assertFalse(audio.playing)
            self.assertFalse(audio.paused)

    def test_iteration_2_negate_guard(self):


        audio = AudioEngine()
        audio.playing = True   # S1
        audio.paused = False   # S2

        with patch('music_player.audio_backend.HAS_PYGAME', True):
            with patch('music_player.audio_backend.pygame') as mock_pygame:

                audio.pause()


                self.assertFalse(audio.playing)
                self.assertTrue(audio.paused)
                mock_pygame.mixer.music.pause.assert_called_once()

    def test_iteration_3_negate_pygame(self):


        audio = AudioEngine()
        audio.playing = True   # S1
        audio.paused = False   # S2

        with patch('music_player.audio_backend.HAS_PYGAME', False):
            with patch('builtins.print') as mock_print:
                audio.pause()


                self.assertFalse(audio.playing)
                self.assertTrue(audio.paused)
                mock_print.assert_called_with("[audio] PAUSE (simulated)")


if __name__ == '__main__':
    unittest.main()