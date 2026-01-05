import unittest
from unittest.mock import patch
from music_player.audio_backend import AudioEngine


class TestConcolicGenerations(unittest.TestCase):

    def test_run_1_initial_seed(self):

        audio = AudioEngine()
        audio.paused = False

        with patch('music_player.audio_backend.HAS_PYGAME', False):
            with patch.object(audio, '_resume_real') as mock_resume_real:
                audio.resume()

                self.assertFalse(audio.playing)
                mock_resume_real.assert_not_called()

    def test_run_2_derived_input(self):

        audio = AudioEngine()
        audio.paused = True

        with patch('music_player.audio_backend.HAS_PYGAME', False):
            with patch('builtins.print') as mock_print:
                audio.resume()

                self.assertTrue(audio.playing)
                mock_print.assert_called_with("[audio] RESUME (simulated)")

    def test_run_3_derived_input(self):

        audio = AudioEngine()
        audio.paused = True

        with patch('music_player.audio_backend.HAS_PYGAME', True):
            with patch.object(audio, '_resume_real') as mock_resume_real:
                audio.resume()

                self.assertTrue(audio.playing)
                mock_resume_real.assert_called_once()


if __name__ == '__main__':
    unittest.main()