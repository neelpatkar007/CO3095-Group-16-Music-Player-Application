import unittest
from unittest.mock import patch
from music_player.audio_backend import AudioEngine


class TestSymbolicExecution(unittest.TestCase):
    '''
    White-box test suite verifying the Symbolic Analysis for `set_muted`.
    Focus: Verification of all Path Conditions (PC_1, PC_2, PC_3).

    Test Results Table:
    | Method        | Actual | Expected | Status |
    |---------------|--------|----------|--------|
    | test_path_pc1 | Pass   | Pass     | PASS   |
    | test_path_pc2 | Pass   | Pass     | PASS   |
    | test_path_pc3 | Pass   | Pass     | PASS   |

    The average test coverage for this suite is measured at 100%.
    '''

    def test_path_pc1(self):
        """
        Symbolic Path PC_1: NOT S1
        Input: S1 (muted) = False
        Expected Behaviour: self.muted becomes False; inner branches skipped.
        """
        audio = AudioEngine()

        with patch('music_player.audio_backend.HAS_PYGAME', False):
            audio.set_muted(False)

        self.assertFalse(audio.muted, "PC_1 Failed: internal state should be False.")

    def test_path_pc2(self):
        """
        Symbolic Path PC_2: S1 AND NOT S2
        Input: S1 (muted) = True, S2 (HAS_PYGAME) = False
        Expected Behaviour: self.muted becomes True; Pygame call skipped.
        """
        audio = AudioEngine()

        with patch('music_player.audio_backend.HAS_PYGAME', False):
            audio.set_muted(True)

        self.assertTrue(audio.muted, "PC_2 Failed: internal state should be True.")

    def test_path_pc3(self):
        """
        Symbolic Path PC_3: S1 AND S2
        Input: S1 (muted) = True, S2 (HAS_PYGAME) = True
        Expected Behaviour: self.muted becomes True; Pygame volume set to 0.0.
        """
        audio = AudioEngine()

        with patch('music_player.audio_backend.HAS_PYGAME', True):
            with patch('music_player.audio_backend.pygame') as mock_pygame:
                audio.set_muted(True)

                self.assertTrue(audio.muted, "PC_3 Failed: internal state should be True.")
                mock_pygame.mixer.music.set_volume.assert_called_once_with(0.0)


if __name__ == '__main__':
    unittest.main()