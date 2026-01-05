import unittest
from unittest.mock import MagicMock, patch
from music_player.audio_backend import AudioEngine

class TestConcolicExecution(unittest.TestCase):

    def test_iter1_path_pc1(self):

        with patch('music_player.audio_backend.HAS_PYGAME', True):
            with patch('music_player.audio_backend.pygame') as mock_pygame:
                mock_pygame.mixer.music.get_busy.return_value = True

                player = AudioEngine()
                player.playing = True

                self.assertTrue(player.is_busy())

    def test_iter2_path_pc2_flip(self):

        with patch('music_player.audio_backend.HAS_PYGAME', False):
            player = AudioEngine()
            player.playing = True
            player.paused = False


            self.assertTrue(player.is_busy())

    def test_iter3_path_pc2_neg(self):

        with patch('music_player.audio_backend.HAS_PYGAME', False):
            player = AudioEngine()
            player.playing = False
            player.paused = False


            self.assertFalse(player.is_busy())


if __name__ == '__main__':
    unittest.main()