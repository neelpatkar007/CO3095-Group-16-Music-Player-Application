import unittest
from unittest.mock import patch
import io
from music_player.audio_backend import AudioEngine


class TestConcolicExecution(unittest.TestCase):

    def test_iteration_1_base_path(self):

        audio = AudioEngine()
        audio.current_path = None
        audio.current_speed = 1.0
        audio.temp_file = None
        audio.muted = False
        audio.volume = 0.8

        S1 = 5.5

        with patch('builtins.print') as mock_print:
            audio._seek_simulated(S1)

            mock_print.assert_called()
            call_args = str(mock_print.call_args)
            self.assertIn('[audio] SEEK', call_args)
            self.assertIn('5.5', call_args)


if __name__ == '__main__':
    unittest.main()