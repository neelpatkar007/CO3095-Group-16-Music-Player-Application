import unittest
from unittest.mock import MagicMock, patch
from music_player.audio_backend import AudioEngine


class TestSymbolicExecution(unittest.TestCase):

    def test_pc1_assertion_failure(self):

        audio = AudioEngine()

        with patch('music_player.audio_backend.pygame', None):
            with self.assertRaises(AssertionError):
                audio._pause_real()

    def test_pc2_nominal_execution(self):

        audio = AudioEngine()
        mock_pygame = MagicMock()

        with patch('music_player.audio_backend.pygame', mock_pygame):
            audio._pause_real()

            mock_pygame.mixer.music.pause.assert_called_once()


if __name__ == '__main__':
    unittest.main()