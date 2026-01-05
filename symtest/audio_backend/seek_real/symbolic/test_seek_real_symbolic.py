import unittest
from unittest.mock import patch, MagicMock
from pathlib import Path
from music_player.audio_backend import AudioEngine

class TestSymbolicExecution(unittest.TestCase):


    def test_pc1_assertion_fail(self):

        audio = AudioEngine()
        audio.current_path = Path("original.mp3")
        audio.current_speed = 1.0
        audio.temp_file = MagicMock(spec=Path)
        audio.temp_file.exists.return_value = False
        audio.temp_file.__str__.return_value = "temp.mp3"
        audio.muted = False
        audio.volume = 0.8

        with patch('music_player.audio_backend.pygame', None):
            with self.assertRaises(AssertionError):
                audio._seek_real(10.0)

    def test_pc2_pc5_speed_mod(self):

        audio = AudioEngine()
        audio.current_path = Path("original.mp3")
        audio.current_speed = 1.5
        audio.temp_file = MagicMock(spec=Path)
        audio.temp_file.exists.return_value = True
        audio.temp_file.__str__.return_value = "temp.mp3"
        audio.muted = False
        audio.volume = 0.8

        with patch('music_player.audio_backend.pygame') as mock_pygame:
            audio._seek_real(30.0)

            mock_pygame.mixer.music.load.assert_called_with(str(audio.temp_file))
            expected_pos = 30.0 / 1.5
            mock_pygame.mixer.music.play.assert_called_with(loops=0, start=expected_pos)
            mock_pygame.mixer.music.set_volume.assert_called_with(0.008)

    def test_pc3_pc4_normal_muted(self):

        audio = AudioEngine()
        audio.current_path = Path("original.mp3")
        audio.current_speed = 1.0
        audio.temp_file = MagicMock(spec=Path)
        audio.temp_file.exists.return_value = False
        audio.temp_file.__str__.return_value = "temp.mp3"
        audio.muted = True
        audio.volume = 0.8

        with patch('music_player.audio_backend.pygame') as mock_pygame:
            audio._seek_real(15.0)

            mock_pygame.mixer.music.load.assert_called_with(str(audio.current_path))
            mock_pygame.mixer.music.set_volume.assert_called_with(0.0)

    def test_pc6_exception_handling(self):

        audio = AudioEngine()
        audio.current_path = Path("original.mp3")
        audio.current_speed = 1.0
        audio.temp_file = MagicMock(spec=Path)
        audio.temp_file.exists.return_value = False
        audio.temp_file.__str__.return_value = "temp.mp3"
        audio.muted = False
        audio.volume = 0.8

        with patch('music_player.audio_backend.pygame') as mock_pygame:
            mock_pygame.mixer.music.load.side_effect = Exception("File Corrupt")

            try:
                audio._seek_real(5.0)
            except:
                self.fail("Function should catch exception internally")


if __name__ == '__main__':
    unittest.main()