import unittest
from unittest.mock import patch
from pathlib import Path
from music_player.audio_backend import AudioEngine


class TestSymbolicExecution(unittest.TestCase):
    """
    White-Box Testing Suite: Symbolic Execution
    Target: _play_simulated

    Test Results Table:
    | Method      | Actual Result           | Expected Result         | Status |
    |-------------|-------------------------|-------------------------|--------|
    | test_PC_1   | Output matches template | Output matches template | PASS   |

    The average test coverage for this suite is measured at 100%.
    """

    def test_PC_1(self):
        """
        Path ID: PC_1
        Condition: True (Unconditional)
        Symbolic Inputs:
            S1 (self) = AudioEngine instance
            S2 (path) = Path object with .name attribute
            S3 (start_pos) = 5.5 (Arbitrary float satisfying constraints)
        """
        audio = AudioEngine()
        test_path = Path("symbolic_track.wav")
        start_pos = 5.5

        with patch('builtins.print') as mock_print:
            audio._play_simulated(test_path, start_pos)

            expected_output = f"[audio] PLAY (simulated) {test_path.name} from {start_pos:.1f}s"
            mock_print.assert_called_once_with(expected_output)


if __name__ == '__main__':
    unittest.main()