import unittest
from unittest.mock import patch
from pathlib import Path
from music_player.audio_backend import AudioEngine


class TestConcolicExecution(unittest.TestCase):

    def test_iteration_1(self):

        audio = AudioEngine()
        test_path = Path("concrete_seed.mp3")

        with patch('builtins.print') as mock_print:
            audio._play_simulated(test_path, 0.0)

            expected_output = f"[audio] PLAY (simulated) {test_path.name} from 0.0s"
            mock_print.assert_called_once_with(expected_output)

if __name__ == '__main__':
    unittest.main()