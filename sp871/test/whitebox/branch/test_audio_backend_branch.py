import unittest
from unittest.mock import MagicMock, patch
from pathlib import Path
from music_player import audio_backend


class TestAudioBackendBranch(unittest.TestCase):


    def setUp(self):
        # Set HAS_PYGAME True
        self.patcher = patch("music_player.audio_backend.HAS_PYGAME", True)
        self.patcher.start()
        self.engine = audio_backend.AudioEngine()

    def tearDown(self):
        self.patcher.stop()

    @patch("music_player.audio_backend.pygame")
    def test_volume_branches(self, mock_pg):
        """
        Expected Result: The code calculates float volume and calls pygame.mixer.music.set_volume.
        Actual Result: Passed. set_volume called with 0.5.
        """
        # Ensure nested if is True
        mock_pg.mixer.music = MagicMock()

        # Call set_volume
        self.engine.set_volume(50)

        # Verify call
        mock_pg.mixer.music.set_volume.assert_called_with(0.5)

    @patch("music_player.audio_backend.pygame")
    def test_seek_branches(self, mock_pg):
        """
        Expected Result:
         - Normal speed loads original file.
         - Modified speed + Temp file loads temp file.
         - Seek position is adjusted by speed factor.
        Actual Result:
            PASSED [100%][audio] SEEK -> 10.0s
            [audio] SEEK -> 20.0s
        """
        self.engine.current_path = Path("orig.mp3")
        self.engine.temp_file = MagicMock()

        # Speed = 1.0
        self.engine.current_speed = 1.0
        self.engine.seek(10.0)
        # Load original file
        mock_pg.mixer.music.load.assert_called_with("orig.mp3")
        mock_pg.mixer.music.play.assert_called_with(loops=0, start=10.0)

        # Speed != 1.0 AND Temp Exists
        self.engine.current_speed = 2.0
        self.engine.temp_file.exists.return_value = True

        self.engine.seek(20.0)
        # Loads temp file
        mock_pg.mixer.music.load.assert_called_with(str(self.engine.temp_file))
        mock_pg.mixer.music.play.assert_called_with(loops=0, start=10.0)

    @patch("music_player.audio_backend.pygame")
    def test_stop_real_coverage(self, mock_pg):
        """
        Expected Result: The _stop_real method calls pygame.mixer.music.stop.
        Actual Result: Passed. Mock assertion confirmed call to pygame.
        """
        self.engine.playing = True
        self.engine.stop()
        mock_pg.mixer.music.stop.assert_called()