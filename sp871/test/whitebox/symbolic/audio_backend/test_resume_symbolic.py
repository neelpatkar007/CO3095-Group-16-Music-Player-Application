import unittest
from unittest.mock import patch
from music_player.audio_backend import AudioEngine


class TestSymbolicExecution(unittest.TestCase):

    def test_pc1_early_return(self):

        audio = AudioEngine()
        audio.paused = False

        with patch.object(audio, '_resume_real') as mock_resume_real:
            audio.resume()

            # Verification
            self.assertFalse(audio.playing, "Violation of PC_1: State should not change if not paused.")
            mock_resume_real.assert_not_called()

    def test_pc2_real_execution(self):

        audio = AudioEngine()
        audio.paused = True

        with patch('music_player.audio_backend.HAS_PYGAME', True):
            with patch.object(audio, '_resume_real') as mock_resume_real:
                audio.resume()

                self.assertFalse(audio.paused, "State mutation failed: paused should be False.")
                self.assertTrue(audio.playing, "State mutation failed: playing should be True.")
                mock_resume_real.assert_called_once()

    def test_pc3_simulated_execution(self):

        audio = AudioEngine()
        audio.paused = True

        with patch('music_player.audio_backend.HAS_PYGAME', False):
            with patch('builtins.print') as mock_print:
                audio.resume()

                # Verification
                self.assertFalse(audio.paused)
                self.assertTrue(audio.playing)
                mock_print.assert_called_with("[audio] RESUME (simulated)")


if __name__ == '__main__':
    unittest.main()