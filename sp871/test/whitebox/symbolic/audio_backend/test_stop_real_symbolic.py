import unittest
from unittest.mock import patch
from music_player.audio_backend import AudioEngine

class TestSymbolicStopReal(unittest.TestCase):

    def test_pc_1_assertion(self):

        audio = AudioEngine()

        with patch('music_player.audio_backend.pygame', None):
            with self.assertRaises(AssertionError):
                audio._stop_real()

    def test_pc_2_nominal_exec(self):

        audio = AudioEngine()

        with patch('music_player.audio_backend.pygame') as mock_pygame:
            audio._stop_real()

            mock_pygame.mixer.music.stop.assert_called_once()


if __name__ == '__main__':
    unittest.main()