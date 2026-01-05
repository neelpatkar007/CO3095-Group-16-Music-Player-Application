import unittest
from unittest.mock import patch
from music_player.audio_backend import AudioEngine


class TestSymbolicExecution(unittest.TestCase):


    def test_path_pc1_idle(self):

        audio = AudioEngine()
        audio.playing = False
        audio.paused = False

        audio.stop()

        self.assertFalse(audio.playing)
        self.assertFalse(audio.paused)

    def test_path_pc2_real(self):

        audio = AudioEngine()
        audio.playing = True
        audio.paused = False

        with patch('music_player.audio_backend.HAS_PYGAME', True):
            with patch('music_player.audio_backend.pygame') as mock_pygame:
                audio.stop()

                self.assertFalse(audio.playing)
                self.assertFalse(audio.paused)

    def test_path_pc3_simulated(self):

        audio = AudioEngine()
        audio.playing = True
        audio.paused = False

        with patch('music_player.audio_backend.HAS_PYGAME', False):
            audio.stop()

            self.assertFalse(audio.playing)
            self.assertFalse(audio.paused)


if __name__ == '__main__':
    unittest.main()