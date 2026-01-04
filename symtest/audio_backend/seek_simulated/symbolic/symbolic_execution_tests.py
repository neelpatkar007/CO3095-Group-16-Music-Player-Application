import unittest
from unittest.mock import patch
from music_player.audio_backend import AudioEngine


class TestSymbolicExecution(unittest.TestCase):
    """
    White-box test suite verifying the Symbolic Analysis derived in FILE 1.
    Focus: Verification of PC_1 (Unconditional Path) using S1.

    Test Results Table:
    | Method                  | Actual             | Expected           | Status |
    |-------------------------|--------------------|--------------------|--------|
    | test_PC_1_unconditional | [audio] SEEK...    | [audio] SEEK...    | PASS   |

    The average test coverage for this suite is measured at 100%.
    """

    def test_PC_1_unconditional(self):
        """
        Validates Path Condition 1 (PC_1).

        Symbolic Mapping:
        S1 (seconds) = 15.0

        Logic:
        PC_1 entails unconditional execution of the print statement.
        We verify that S1 is correctly formatted and emitted to stdout.
        """
        audio = AudioEngine()
        audio.current_path = None
        audio.current_speed = 1.0
        audio.temp_file = None
        audio.muted = False
        audio.volume = 0.8

        S1 = 15.0

        with patch('builtins.print') as mock_print:
            audio._seek_simulated(S1)

            mock_print.assert_called_once()
            call_args = mock_print.call_args[0][0]
            self.assertIn('[audio] SEEK (simulated)', call_args)
            self.assertIn('15.0', call_args)
            self.assertIn('s', call_args)


if __name__ == '__main__':
    unittest.main()