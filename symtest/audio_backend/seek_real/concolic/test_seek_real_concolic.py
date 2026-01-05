import unittest
from unittest.mock import patch, MagicMock
from pathlib import Path
from music_player.audio_backend import AudioEngine


class TestConcolicExecution(unittest.TestCase):

    def test_iteration_1_base_case(self):

        audio = AudioEngine()
        audio.current_path = Path("song.mp3")
        audio.current_speed = 1.0
        audio.temp_file = MagicMock(spec=Path)
        audio.temp_file.exists.return_value = False
        audio.temp_file.__str__.return_value = "temp.mp3"
        audio.volume = 0.5
        audio.muted = False

        with patch('music_player.audio_backend.pygame') as mock_pygame:
            audio._seek_real(10.0)

            mock_pygame.mixer.music.load.assert_called_with(str(audio.current_path))
            mock_pygame.mixer.music.play.assert_called_with(loops=0, start=10.0)
            mock_pygame.mixer.music.set_volume.assert_called_with(0.005)

    def test_iteration_2_flip_speed(self):

        audio = AudioEngine()
        audio.current_path = Path("song.mp3")
        audio.current_speed = 1.5
        audio.temp_file = MagicMock(spec=Path)
        audio.temp_file.exists.return_value = True
        audio.temp_file.__str__.return_value = "temp.mp3"
        audio.volume = 0.5
        audio.muted = False

        with patch('music_player.audio_backend.pygame') as mock_pygame:
            audio._seek_real(10.0)

            mock_pygame.mixer.music.load.assert_called_with(str(audio.temp_file))
            call_args = mock_pygame.mixer.music.play.call_args
            self.assertAlmostEqual(call_args.kwargs['start'], 6.666, places=2)
            mock_pygame.mixer.music.set_volume.assert_called_with(0.005)

    def test_iteration_3_flip_mute(self):

        audio = AudioEngine()
        audio.current_path = Path("song.mp3")
        audio.current_speed = 1.5
        audio.temp_file = MagicMock(spec=Path)
        audio.temp_file.exists.return_value = True
        audio.temp_file.__str__.return_value = "temp.mp3"
        audio.volume = 0.5
        audio.muted = True

        with patch('music_player.audio_backend.pygame') as mock_pygame:
            audio._seek_real(10.0)

            mock_pygame.mixer.music.set_volume.assert_called_with(0.0)

    def test_iteration_4_force_exception(self):

        audio = AudioEngine()
        audio.current_path = Path("song.mp3")
        audio.current_speed = 1.0
        audio.temp_file = MagicMock(spec=Path)
        audio.temp_file.exists.return_value = False
        audio.temp_file.__str__.return_value = "temp.mp3"
        audio.muted = False

        with patch('music_player.audio_backend.pygame') as mock_pygame:
            mock_pygame.mixer.music.load.side_effect = RuntimeError("Concolic Injection")

            try:
                audio._seek_real(10.0)
            except:
                self.fail("Function should catch exception internally")


if __name__ == '__main__':
    unittest.main()