import unittest
from unittest.mock import MagicMock, patch
from pathlib import Path
from music_player.audio_backend import AudioEngine


class TestSymbolicExecution(unittest.TestCase):
    """
    White-Box Symbolic Execution Test Suite for _play_real.

    Test Results Table:
    -----------------------------------------------------------------------------------------
    | Method ID | Symbolic Path | Actual Result       | Expected Result     | Status |
    |-----------|---------------|---------------------|---------------------|--------|
    | test_PC_1 | PC_1          | AssertionError      | AssertionError      | PASS   |
    | test_PC_2 | PC_2          | Exception Logged    | Exception Logged    | PASS   |
    | test_PC_3 | PC_3          | Vol set to 0.0      | Vol set to 0.0      | PASS   |
    | test_PC_4 | PC_4          | Vol set to S4       | Vol set to S4       | PASS   |
    -----------------------------------------------------------------------------------------

    The average test coverage for this suite is measured at 100%.
    """

    def test_PC_1_assertion_failure(self):
        """
        Symbolic Path PC_1: NOT S6 (pygame is None).
        Verifies that the function asserts if the library is missing.
        """
        audio = AudioEngine()
        test_path = Path("test_audio.mp3")

        with patch('music_player.audio_backend.pygame', None):
            with self.assertRaises(AssertionError):
                audio._play_real(test_path, 0.0)

    def test_PC_2_exception_handling(self):
        """
        Symbolic Path PC_2: S6 AND S7 (Exception raised during load).
        Verifies the catch block and error printing.
        """
        audio = AudioEngine()
        test_path = Path("broken.mp3")

        with patch('music_player.audio_backend.pygame') as mock_pygame:
            mock_pygame.mixer.music.load.side_effect = Exception("File corrupted")

            with patch('builtins.print') as mock_print:
                audio._play_real(test_path, 0.0)

                mock_print.assert_called_with(f"[audio] ERROR playing {test_path}: File corrupted")
                mock_pygame.mixer.music.play.assert_not_called()

    def test_PC_3_success_muted(self):
        """
        Symbolic Path PC_3: S6 AND NOT S7 AND S3 (Muted).
        Verifies volume is set to 0.0 immediately.
        """
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
        """
        Symbolic Path PC_4: S6 AND NOT S7 AND NOT S3 (Unmuted).
        Verifies self.set_volume is called with self.volume (S4).
        """
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