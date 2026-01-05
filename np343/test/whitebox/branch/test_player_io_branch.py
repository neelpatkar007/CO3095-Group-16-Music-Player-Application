import os
import unittest
from unittest.mock import MagicMock
from music_player import player_io


class TestPlayerIO(unittest.TestCase):
    """
    Whitebox Branch Testing for player_io.py.
    Tool: Python unittest + unittest.mock
    Technique: White-Box Branch Testing
    """
    def test_export_playlist_creates_file(self):
        """
        Expected Result: The file "test_export.m3u" is created and contains the header "#EXTM3U".
        Actual Result:
            [export] Exporting playlist 'MyMix'...
            [export] Saved 1 songs to test_export.m3u. Visible after close.
        """
        mock_track = MagicMock()
        mock_track.duration_seconds = 120
        mock_track.display_name = "Test Song"
        mock_track.path.resolve.return_value = "/path/to/song.mp3"

        mock_playlist = MagicMock()
        mock_playlist.name = "MyMix"
        mock_playlist.tracks = [mock_track]

        mock_state = MagicMock()
        mock_state.playlists = [mock_playlist]

        filename = "test_export.m3u"
        player_io.export_playlist(mock_state, "MyMix", filename)

        self.assertTrue(os.path.exists(filename))
        with open(filename, "r") as f:
            content = f.read()
            self.assertIn("#EXTM3U", content)
            self.assertIn("Test Song", content)

        if os.path.exists(filename):
            os.remove(filename)