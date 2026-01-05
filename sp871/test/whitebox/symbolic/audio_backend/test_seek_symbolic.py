import unittest
from unittest.mock import patch
from music_player.audio_backend import AudioEngine


class TestSymbolicExecution(unittest.TestCase):


    def test_PC_1_early_return(self):

        audio = AudioEngine()
        audio.current_path = None

        with patch.object(audio, '_seek_real') as mock_seek_real:
            with patch.object(audio, '_seek_simulated') as mock_seek_simulated:
                audio.seek(5.0)

                self.assertFalse(audio.playing, "S1: State should remain playing=False")
                mock_seek_real.assert_not_called()
                mock_seek_simulated.assert_not_called()

    def test_PC_2_seek_real(self):

        audio = AudioEngine()
        audio.current_path = "track.mp3"

        with patch('music_player.audio_backend.HAS_PYGAME', True):
            with patch.object(audio, '_seek_real') as mock_seek_real:
                audio.seek(15.0)

                self.assertTrue(audio.playing, "State should be updated to playing=True")
                self.assertFalse(audio.paused, "State should be updated to paused=False")
                mock_seek_real.assert_called_once_with(15.0)

    def test_PC_3_seek_simulated(self):

        audio = AudioEngine()
        audio.current_path = "track.mp3"

        with patch('music_player.audio_backend.HAS_PYGAME', False):
            with patch.object(audio, '_seek_simulated') as mock_seek_simulated:
                audio.seek(30.0)

                self.assertTrue(audio.playing, "State should be updated to playing=True")
                self.assertFalse(audio.paused, "State should be updated to paused=False")
                mock_seek_simulated.assert_called_once_with(30.0)


if __name__ == '__main__':
    unittest.main()