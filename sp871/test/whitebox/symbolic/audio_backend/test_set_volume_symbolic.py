import unittest
from unittest.mock import patch
from music_player.audio_backend import AudioEngine


class TestSymbolicExecution(unittest.TestCase):


    def test_path_pc1_full(self):

        audio = AudioEngine()
        S1_value = 50

        with patch('music_player.audio_backend.HAS_PYGAME', True):
            with patch('music_player.audio_backend.pygame') as mock_pygame:
                audio.set_volume(S1_value)

                self.assertEqual(audio.volume, 50)
                mock_pygame.mixer.music.set_volume.assert_called_once_with(0.5)

    def test_path_pc2_part(self):

        audio = AudioEngine()
        S1_value = 50

        with patch('music_player.audio_backend.HAS_PYGAME', True):
            with patch('music_player.audio_backend.pygame') as mock_pygame:
                mock_pygame.mixer = None
                audio.set_volume(S1_value)

                self.assertEqual(audio.volume, 50)

    def test_path_pc3_neg(self):

        audio = AudioEngine()
        S1_value = 50

        with patch('music_player.audio_backend.HAS_PYGAME', False):
            audio.set_volume(S1_value)

            self.assertEqual(audio.volume, 50)


if __name__ == '__main__':
    unittest.main()