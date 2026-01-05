import unittest
from unittest.mock import MagicMock, patch
from pathlib import Path
from music_player.audio_backend import AudioEngine


class TestSymbolicExecution(unittest.TestCase):

    def test_PC_1_assertion_failure(self):

        audio = AudioEngine()
        test_path = Path("test_audio.mp3")

        with patch('music_player.audio_backend.pygame', None):
            with self.assertRaises(AssertionError):
                audio._play_real(test_path, 0.0)

    def test_PC_2_exception_handling(self):

        audio = AudioEngine()
        test_path = Path("broken.mp3")

        with patch('music_player.audio_backend.pygame') as mock_pygame:
            mock_pygame.mixer.music.load.side_effect = Exception("File corrupted")

            with patch('builtins.print') as mock_print:
                audio._play_real(test_path, 0.0)

                mock_print.assert_called_with(f"[audio] ERROR playing {test_path}: File corrupted")
                mock_pygame.mixer.music.play.assert_not_called()

    def test_PC_3_success_muted(self):

        audio = AudioEngine()
        audio.muted = True
        test_path = Path("song.mp3")

        with patch('music_player.audio_backend.pygame') as mock_pygame:
            with patch.object(audio, 'set_volume') as mock_set_volume:
                with patch('builtins.print') as mock_print:
                    audio._play_real(test_path, 5.0)

                    mock_pygame.mixer.music.load.assert_called_with(str(test_path))
                    mock_pygame.mixer.music.play.assert_called_with(loops=0, start=5.0)
                    mock_pygame.mixer.music.set_volume.assert_called_with(0.0)
                    mock_set_volume.assert_not_called()

                    expected_msg = f"[audio] PLAY (real) {test_path.name} from 5.0s (Speed: {audio.current_speed}x)"
                    mock_print.assert_called_with(expected_msg)

    def test_PC_4_success_unmuted(self):

        audio = AudioEngine()
        audio.muted = False
        audio.volume = 0.8
        test_path = Path("song.mp3")

        with patch('music_player.audio_backend.pygame') as mock_pygame:
            with patch.object(audio, 'set_volume') as mock_set_volume:
                audio._play_real(test_path, 0.0)

                mock_set_volume.assert_called_with(0.8)
                mock_pygame.mixer.music.set_volume.assert_not_called()


if __name__ == '__main__':
    unittest.main()