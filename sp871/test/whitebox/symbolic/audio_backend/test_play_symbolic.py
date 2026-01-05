import unittest
from unittest.mock import patch, Mock
from pathlib import Path
from music_player.audio_backend import AudioEngine


class TestSymbolicExecution(unittest.TestCase):


    def test_PC_1_standard_playback_real(self):

        audio = AudioEngine()
        test_path = Path("/music/song.mp3")

        with patch('music_player.audio_backend.HAS_PYDUB', False):
            with patch('music_player.audio_backend.HAS_PYGAME', True):
                with patch.object(audio, '_play_real') as mock_play_real:
                    audio.play(test_path, start_pos=5.0, speed=1.0)
                    mock_play_real.assert_called_once_with(test_path, 5.0)

    def test_PC_2_standard_playback_simulated(self):

        audio = AudioEngine()
        test_path = Path("/music/song.mp3")

        with patch('music_player.audio_backend.HAS_PYDUB', False):
            with patch('music_player.audio_backend.HAS_PYGAME', False):
                with patch.object(audio, '_play_simulated') as mock_play_sim:
                    audio.play(test_path, start_pos=5.0, speed=1.0)
                    mock_play_sim.assert_called_once_with(test_path, 5.0)

    def test_PC_3_speed_processing_success_real(self):

        audio = AudioEngine()
        test_path = Path("/music/song.mp3")

        with patch('music_player.audio_backend.HAS_PYDUB', True):
            with patch('music_player.audio_backend.HAS_PYGAME', True):
                # No AudioSegment patch needed
                with patch.object(audio, '_play_real') as mock_play_real:
                    audio.play(test_path, start_pos=5.0, speed=1.5)
                    mock_play_real.assert_called_once_with(test_path, 5.0)

    def test_PC_4_speed_processing_success_simulated(self):

        audio = AudioEngine()
        test_path = Path("/music/song.mp3")

        with patch('music_player.audio_backend.HAS_PYDUB', True):
            with patch('music_player.audio_backend.HAS_PYGAME', False):
                # No AudioSegment patch needed
                with patch.object(audio, '_play_simulated') as mock_play_sim:
                    audio.play(test_path, start_pos=5.0, speed=1.5)
                    mock_play_sim.assert_called_once_with(test_path, 5.0)

    def test_PC_5_speed_processing_failure_real(self):

        audio = AudioEngine()
        test_path = Path("/music/song.mp3")

        with patch('music_player.audio_backend.HAS_PYDUB', True):
            with patch('music_player.audio_backend.HAS_PYGAME', True):
                # No AudioSegment patch needed
                with patch.object(audio, '_play_real') as mock_play_real:
                    audio.play(test_path, start_pos=5.0, speed=1.5)
                    self.assertEqual(audio.current_speed, 1.0)
                    mock_play_real.assert_called_once_with(test_path, 5.0)

    def test_PC_6_speed_processing_failure_simulated(self):

        audio = AudioEngine()
        test_path = Path("/music/song.mp3")

        with patch('music_player.audio_backend.HAS_PYDUB', True):
            with patch('music_player.audio_backend.HAS_PYGAME', False):
                with patch.object(audio, '_play_simulated') as mock_play_sim:
                    audio.play(test_path, start_pos=5.0, speed=1.5)
                    self.assertEqual(audio.current_speed, 1.0)
                    mock_play_sim.assert_called_once_with(test_path, 5.0)


if __name__ == '__main__':
    unittest.main()
