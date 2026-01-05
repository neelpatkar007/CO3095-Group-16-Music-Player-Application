import unittest
from unittest.mock import MagicMock, patch
from pathlib import Path
from music_player.audio_backend import AudioEngine


class TestConcolicTesting(unittest.TestCase):

    def test_iteration_1_seed_execution(self):

        audio = AudioEngine()
        audio.muted = False
        test_path = Path("seed.mp3")

        with patch('music_player.audio_backend.pygame') as mock_pygame:
            with patch.object(audio, 'set_volume') as mock_set_volume:
                audio._play_real(test_path, 0.0)

                mock_set_volume.assert_called()
                mock_pygame.mixer.music.set_volume.assert_not_called()

    def test_iteration_2_flip_mute_constraint(self):

        audio = AudioEngine()
        audio.muted = True
        test_path = Path("seed.mp3")

        with patch('music_player.audio_backend.pygame') as mock_pygame:
            with patch.object(audio, 'set_volume') as mock_set_volume:
                audio._play_real(test_path, 0.0)

                mock_pygame.mixer.music.set_volume.assert_called_with(0.0)
                mock_set_volume.assert_not_called()

    def test_iteration_3_flip_exception_constraint(self):

        audio = AudioEngine()
        audio.muted = True
        test_path = Path("seed.mp3")

        with patch('music_player.audio_backend.pygame') as mock_pygame:
            mock_pygame.mixer.music.load.side_effect = Exception("Concolic Injection")

            with patch('builtins.print') as mock_print:
                audio._play_real(test_path, 0.0)

                mock_print.assert_called_with(f"[audio] ERROR playing {test_path}: Concolic Injection")

    def test_iteration_4_flip_pygame_constraint(self):

        audio = AudioEngine()
        test_path = Path("seed.mp3")

        with patch('music_player.audio_backend.pygame', None):
            with self.assertRaises(AssertionError):
                audio._play_real(test_path, 0.0)

if __name__ == '__main__':
    unittest.main()