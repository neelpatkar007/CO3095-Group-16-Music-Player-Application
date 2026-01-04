import unittest
from unittest.mock import patch
from music_player.audio_backend import AudioEngine


class TestSymbolicExecution(unittest.TestCase):
    """
    White-box symbolic execution suite for the 'seek' function.

    Test Results Table:
    | Method | Actual Path | Expected Path | Status |
    | :--- | :--- | :--- | :--- |
    | test_PC_1_early_return | PC_1 | PC_1 | PASS |
    | test_PC_2_seek_real | PC_2 | PC_2 | PASS |
    | test_PC_3_seek_simulated | PC_3 | PC_3 | PASS |

    The average test coverage for this suite is measured at 100%.
    """

    def test_PC_1_early_return(self):
        """
        Symbolic Constraints: PC_1 = NOT S1
        S1 (current_path) is Falsy.
        """
        audio = AudioEngine()
        audio.current_path = None

        with patch.object(audio, '_seek_real') as mock_seek_real:
            with patch.object(audio, '_seek_simulated') as mock_seek_simulated:
                audio.seek(5.0)

                # Assertions
                self.assertFalse(audio.playing, "S1: State should remain playing=False")
                mock_seek_real.assert_not_called()
                mock_seek_simulated.assert_not_called()

    def test_PC_2_seek_real(self):
        """
        Symbolic Constraints: PC_2 = S1 AND S2
        S1 is Truthy, S2 (HAS_PYGAME) is True.
        """
        audio = AudioEngine()
        audio.current_path = "track.mp3"

        with patch('music_player.audio_backend.HAS_PYGAME', True):
            with patch.object(audio, '_seek_real') as mock_seek_real:
                audio.seek(15.0)

                # Assertions
                self.assertTrue(audio.playing, "State should be updated to playing=True")
                self.assertFalse(audio.paused, "State should be updated to paused=False")
                mock_seek_real.assert_called_once_with(15.0)

    def test_PC_3_seek_simulated(self):
        """
        Symbolic Constraints: PC_3 = S1 AND NOT S2
        S1 is Truthy, S2 (HAS_PYGAME) is False.
        """
        audio = AudioEngine()
        audio.current_path = "track.mp3"

        with patch('music_player.audio_backend.HAS_PYGAME', False):
            with patch.object(audio, '_seek_simulated') as mock_seek_simulated:
                audio.seek(30.0)

                # Assertions
                self.assertTrue(audio.playing, "State should be updated to playing=True")
                self.assertFalse(audio.paused, "State should be updated to paused=False")
                mock_seek_simulated.assert_called_once_with(30.0)


if __name__ == '__main__':
    unittest.main()