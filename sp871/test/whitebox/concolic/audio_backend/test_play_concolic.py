import unittest
from unittest.mock import patch, Mock
from pathlib import Path
from music_player.audio_backend import AudioEngine


class TestConcolicGenerative(unittest.TestCase):

    def test_iteration_1_baseline(self):
        audio = AudioEngine()
        test_path = Path("/music/test.mp3")

        with patch('music_player.audio_backend.HAS_PYDUB', False):
            with patch('music_player.audio_backend.HAS_PYGAME', True):
                with patch.object(audio, '_play_real') as mock_play_real:
                    audio.play(test_path, start_pos=0.0, speed=1.0)
                    mock_play_real.assert_called_once_with(test_path, 0.0)

    def test_iteration_2_flip_pygame(self):
        audio = AudioEngine()
        test_path = Path("/music/test.mp3")

        with patch('music_player.audio_backend.HAS_PYDUB', False):
            with patch('music_player.audio_backend.HAS_PYGAME', False):
                with patch.object(audio, '_play_simulated') as mock_play_sim:
                    audio.play(test_path, start_pos=0.0, speed=1.0)
                    mock_play_sim.assert_called_once_with(test_path, 0.0)

    def test_iteration_3_flip_speed_and_pydub(self):
        audio = AudioEngine()
        test_path = Path("/music/test.mp3")

        with patch('music_player.audio_backend.HAS_PYDUB', True):
            with patch('music_player.audio_backend.HAS_PYGAME', True):
                with patch.object(audio, '_play_real') as mock_play_real:
                    audio.play(test_path, start_pos=0.0, speed=1.5)
                    mock_play_real.assert_called_once_with(test_path, 0.0)

    def test_iteration_4_flip_pygame_revisit(self):
        audio = AudioEngine()
        test_path = Path("/music/test.mp3")

        with patch('music_player.audio_backend.HAS_PYDUB', True):
            with patch('music_player.audio_backend.HAS_PYGAME', False):
                with patch.object(audio, '_play_simulated') as mock_play_sim:
                    audio.play(test_path, start_pos=0.0, speed=1.5)
                    mock_play_sim.assert_called_once_with(test_path, 0.0)

    def test_iteration_5_flip_exception(self):
        audio = AudioEngine()
        test_path = Path("/music/test.mp3")

        with patch('music_player.audio_backend.HAS_PYDUB', True):
            with patch('music_player.audio_backend.HAS_PYGAME', True):
                with patch.object(audio, '_play_real') as mock_play_real:
                    audio.play(test_path, start_pos=0.0, speed=1.5)
                    mock_play_real.assert_called_once_with(test_path, 0.0)
                    self.assertEqual(audio.current_speed, 1.0)

    def test_iteration_6_flip_exception_simulated(self):
        audio = AudioEngine()
        test_path = Path("/music/test.mp3")

        with patch('music_player.audio_backend.HAS_PYDUB', True):
            with patch('music_player.audio_backend.HAS_PYGAME', False):
                # No AudioSegment patch needed; just test simulated playback
                with patch.object(audio, '_play_simulated') as mock_play_sim:
                    audio.play(test_path, start_pos=0.0, speed=1.5)
                    mock_play_sim.assert_called_once_with(test_path, 0.0)


if __name__ == '__main__':
    unittest.main()
