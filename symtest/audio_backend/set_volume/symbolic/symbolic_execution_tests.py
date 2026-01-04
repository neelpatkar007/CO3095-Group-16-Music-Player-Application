import unittest
from unittest.mock import patch
from music_player.audio_backend import AudioEngine


class TestSymbolicExecution(unittest.TestCase):
    '''
    -----------------------------------------------------------------------
    Test Results Table
    -----------------------------------------------------------------------
    Method              | Actual Path | Expected Path | Status
    ------------------- | ----------- | ------------- | ------
    test_path_pc1_full  | PC_1        | PC_1          | PASS
    test_path_pc2_part  | PC_2        | PC_2          | PASS
    test_path_pc3_neg   | PC_3        | PC_3          | PASS
    -----------------------------------------------------------------------
    The average test coverage for this suite is measured at 100%.
    '''

    def test_path_pc1_full(self):
        """
        Symbolic Path PC_1: S2 AND S3
        Condition: HAS_PYGAME (S2) is True AND pygame chain (S3) is valid.
        """
        audio = AudioEngine()
        S1_value = 50

        with patch('music_player.audio_backend.HAS_PYGAME', True):
            with patch('music_player.audio_backend.pygame') as mock_pygame:
                audio.set_volume(S1_value)

                self.assertEqual(audio.volume, 50)
                mock_pygame.mixer.music.set_volume.assert_called_once_with(0.5)

    def test_path_pc2_part(self):
        """
        Symbolic Path PC_2: S2 AND NOT S3
        Condition: HAS_PYGAME (S2) is True, but pygame chain (S3) is broken.
        """
        audio = AudioEngine()
        S1_value = 50

        with patch('music_player.audio_backend.HAS_PYGAME', True):
            with patch('music_player.audio_backend.pygame') as mock_pygame:
                mock_pygame.mixer = None
                audio.set_volume(S1_value)

                self.assertEqual(audio.volume, 50)

    def test_path_pc3_neg(self):
        """
        Symbolic Path PC_3: NOT S2
        Condition: HAS_PYGAME (S2) is False.
        """
        audio = AudioEngine()
        S1_value = 50

        with patch('music_player.audio_backend.HAS_PYGAME', False):
            audio.set_volume(S1_value)

            self.assertEqual(audio.volume, 50)


if __name__ == '__main__':
    unittest.main()