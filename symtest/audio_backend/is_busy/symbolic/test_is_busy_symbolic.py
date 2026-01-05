import unittest
from unittest.mock import MagicMock, patch
from music_player.audio_backend import AudioEngine

class TestSymbolicExecution(unittest.TestCase):

    def test_pc1_pygame_active(self):

        with patch('music_player.audio_backend.HAS_PYGAME', True):
            with patch('music_player.audio_backend.pygame') as mock_pygame:
                mock_pygame.mixer.music.get_busy.return_value = True

                player = AudioEngine()
                player.playing = False
                player.paused = False

                result = player.is_busy()
                self.assertTrue(result, "PC_1 failed: Should return S4 (True) when S1 is True")

    def test_pc2_internal_logic_true(self):

        with patch('music_player.audio_backend.HAS_PYGAME', False):
            player = AudioEngine()
            player.playing = True
            player.paused = False

            result = player.is_busy()
            self.assertTrue(result, "PC_2 failed: Should return True when playing is True and paused is False")

    def test_pc2_internal_logic_false(self):

        with patch('music_player.audio_backend.HAS_PYGAME', False):
            player = AudioEngine()
            player.playing = True
            player.paused = True

            result = player.is_busy()
            self.assertFalse(result, "PC_2 failed: Should return False when both playing and paused are True")


if __name__ == '__main__':
    unittest.main()