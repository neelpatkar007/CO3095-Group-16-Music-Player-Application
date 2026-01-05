import unittest
from unittest.mock import MagicMock, patch
from music_player.audio_backend import AudioEngine

class TestSymbolicExecution(unittest.TestCase):


    def test_PC1_early_return(self):


        audio = AudioEngine()
        audio.playing = False  # S1
        audio.paused = False   # S2

        with patch('music_player.audio_backend.HAS_PYGAME', True):
            audio.pause()

            self.assertFalse(audio.playing, "S1 should remain False in PC_1")
            self.assertFalse(audio.paused, "S2 should remain False in PC_1")

    def test_PC2_real_pause(self):

        audio = AudioEngine()
        audio.playing = True
        audio.paused = False

        with patch('music_player.audio_backend.HAS_PYGAME', True):
            with patch('music_player.audio_backend.pygame') as mock_pygame:
                audio.pause()

                self.assertFalse(audio.playing, "S1 should update to False in PC_2")
                self.assertTrue(audio.paused, "S2 should update to True in PC_2")
                mock_pygame.mixer.music.pause.assert_called_once()

    def test_PC3_simulated_pause(self):

        audio = AudioEngine()
        audio.playing = True   # S1
        audio.paused = False   # S2

        with patch('music_player.audio_backend.HAS_PYGAME', False):
            with patch('builtins.print') as mock_print:
                audio.pause()

                self.assertFalse(audio.playing, "S1 should update to False in PC_3")
                self.assertTrue(audio.paused, "S2 should update to True in PC_3")
                mock_print.assert_called_with("[audio] PAUSE (simulated)")


if __name__ == '__main__':
    unittest.main()