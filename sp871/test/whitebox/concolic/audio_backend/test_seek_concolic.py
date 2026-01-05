import unittest
from unittest.mock import patch
from music_player.audio_backend import AudioEngine


class TestConcolicExecution(unittest.TestCase):


    def test_iteration_1_base_case(self):

        audio = AudioEngine()
        audio.current_path = None
        seconds = 10.0

        with patch('music_player.audio_backend.HAS_PYGAME', False):
            with patch.object(audio, '_seek_real') as mock_seek_real:
                with patch.object(audio, '_seek_simulated') as mock_seek_simulated:
                    audio.seek(seconds)

                    self.assertFalse(audio.playing)
                    mock_seek_real.assert_not_called()
                    mock_seek_simulated.assert_not_called()

    def test_iteration_2_flip_S1(self):

        audio = AudioEngine()
        audio.current_path = "valid_path.wav"
        seconds = 10.0

        with patch('music_player.audio_backend.HAS_PYGAME', False):
            with patch.object(audio, '_seek_simulated') as mock_seek_simulated:
                audio.seek(seconds)

                self.assertTrue(audio.playing)
                mock_seek_simulated.assert_called_with(seconds)

    def test_iteration_3_flip_S2(self):

        audio = AudioEngine()
        audio.current_path = "valid_path.wav"
        seconds = 10.0

        with patch('music_player.audio_backend.HAS_PYGAME', True):
            with patch.object(audio, '_seek_real') as mock_seek_real:
                audio.seek(seconds)

                self.assertTrue(audio.playing)
                mock_seek_real.assert_called_with(seconds)


if __name__ == '__main__':
    unittest.main()