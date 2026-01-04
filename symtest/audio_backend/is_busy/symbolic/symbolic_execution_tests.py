import unittest
from unittest.mock import MagicMock, patch
from music_player.audio_backend import AudioEngine


class TestSymbolicExecution(unittest.TestCase):
    """
    White-box testing suite derived from Symbolic Analysis (FILE 1).
    Variables mapped: S1 (HAS_PYGAME), S2 (playing), S3 (paused), S4 (get_busy).
    """

    def test_pc1_pygame_active(self):
        """
        Path Condition 1 (PC_1): S1 is True.
        Logic: Returns S4.
        """
        # Symbolic Input Configuration
        with patch('music_player.audio_backend.HAS_PYGAME', True):
            with patch('music_player.audio_backend.pygame') as mock_pygame:
                mock_pygame.mixer.music.get_busy.return_value = True  # S4 = True

                # S2 and S3 are irrelevant in PC_1, but initialized to default
                player = AudioEngine()
                player.playing = False
                player.paused = False

                # Execution & Assertion
                result = player.is_busy()
                self.assertTrue(result, "PC_1 failed: Should return S4 (True) when S1 is True")

    def test_pc2_internal_logic_true(self):
        """
        Path Condition 2 (PC_2): S1 is False.
        Logic: Returns S2 AND NOT S3.
        Case: S2=True, S3=False -> Result True.
        """
        # Symbolic Input Configuration
        with patch('music_player.audio_backend.HAS_PYGAME', False):
            # S2 = True, S3 = False
            player = AudioEngine()
            player.playing = True
            player.paused = False

            # Execution & Assertion
            result = player.is_busy()
            self.assertTrue(result, "PC_2 failed: Should return True when playing is True and paused is False")

    def test_pc2_internal_logic_false(self):
        """
        Path Condition 2 (PC_2): S1 is False.
        Logic: Returns S2 AND NOT S3.
        Case: S2=True, S3=True -> Result False (Boundary check).
        """
        # Symbolic Input Configuration
        with patch('music_player.audio_backend.HAS_PYGAME', False):
            # S2 = True, S3 = True
            player = AudioEngine()
            player.playing = True
            player.paused = True

            # Execution & Assertion
            result = player.is_busy()
            self.assertFalse(result, "PC_2 failed: Should return False when both playing and paused are True")


if __name__ == '__main__':
    unittest.main()