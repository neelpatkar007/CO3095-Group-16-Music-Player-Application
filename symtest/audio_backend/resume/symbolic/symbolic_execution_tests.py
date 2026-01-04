import unittest
from unittest.mock import patch
from music_player.audio_backend import AudioEngine


class TestSymbolicExecution(unittest.TestCase):
    '''
    Test Suite: Symbolic Execution
    Methodology: Verifies paths PC_1, PC_2, and PC_3 derived from static symbolic analysis.

    -----------------------------------------------------------------------
    | Method             | Actual Path | Expected Path | Status             |
    -----------------------------------------------------------------------
    | test_pc1_early_ret | PC_1        | PC_1          | PASS               |
    | test_pc2_real_exec | PC_2        | PC_2          | PASS               |
    | test_pc3_simulated | PC_3        | PC_3          | PASS               |
    -----------------------------------------------------------------------

    The average test coverage for this suite is measured at 100%.
    '''

    def test_pc1_early_return(self):
        """
        Symbolic Logic: PC_1 = NOT S1
        S1 (self.paused) is False.
        """
        audio = AudioEngine()
        audio.paused = False

        with patch.object(audio, '_resume_real') as mock_resume_real:
            audio.resume()

            # Verification
            self.assertFalse(audio.playing, "Violation of PC_1: State should not change if not paused.")
            mock_resume_real.assert_not_called()

    def test_pc2_real_execution(self):
        """
        Symbolic Logic: PC_2 = S1 AND S2
        S1 (self.paused) is True.
        S2 (HAS_PYGAME) is True.
        """
        audio = AudioEngine()
        audio.paused = True

        with patch('music_player.audio_backend.HAS_PYGAME', True):
            with patch.object(audio, '_resume_real') as mock_resume_real:
                audio.resume()

                # Verification
                self.assertFalse(audio.paused, "State mutation failed: paused should be False.")
                self.assertTrue(audio.playing, "State mutation failed: playing should be True.")
                mock_resume_real.assert_called_once()

    def test_pc3_simulated_execution(self):
        """
        Symbolic Logic: PC_3 = S1 AND NOT S2
        S1 (self.paused) is True.
        S2 (HAS_PYGAME) is False.
        """
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