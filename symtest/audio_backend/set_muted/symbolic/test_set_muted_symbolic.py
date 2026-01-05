import unittest
from unittest.mock import patch
from music_player.audio_backend import AudioEngine


class TestSymbolicExecution(unittest.TestCase):


    def test_path_pc1(self):

        audio = AudioEngine()

        with patch('music_player.audio_backend.HAS_PYGAME', False):
            audio.set_muted(False)

        self.assertFalse(audio.muted, "PC_1 Failed: internal state should be False.")

    def test_path_pc2(self):

        audio = AudioEngine()

        with patch('music_player.audio_backend.HAS_PYGAME', False):
            audio.set_muted(True)

        self.assertTrue(audio.muted, "PC_2 Failed: internal state should be True.")

    def test_path_pc3(self):

        audio = AudioEngine()

        with patch('music_player.audio_backend.HAS_PYGAME', True):
            with patch('music_player.audio_backend.pygame') as mock_pygame:
                audio.set_muted(True)

                self.assertTrue(audio.muted, "PC_3 Failed: internal state should be True.")
                mock_pygame.mixer.music.set_volume.assert_called_once_with(0.0)


if __name__ == '__main__':
    unittest.main()