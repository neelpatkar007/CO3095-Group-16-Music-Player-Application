import io
import unittest
import tempfile
from pathlib import Path
from contextlib import redirect_stdout
from unittest.mock import MagicMock

from music_player import player_io
from music_player.player_state import PlayerState


class TestPlayerIoBlackBoxSpec(unittest.TestCase):
    """
    Black-box specification tests for player_io.py.
    Tools -  Python unittest + unittest.mock + tempfile + contextlib.redirect_stdout
    Technique -  Black-Box Specification Testing
    """

    def setUp(self):
        self.state = MagicMock(spec=PlayerState)
        self.state.library_tracks = []
        self.state.tracks = []

    def _capture_prints(self, func, *args, **kwargs) -> str:
        buf = io.StringIO()
        with redirect_stdout(buf):
            func(*args, **kwargs)
        return buf.getvalue()

    # Import Song Tests

    def test_import_song_empty_input_prints_usage(self):
        """
        Expected Result is that it Prints usage when input path is empty.
        Actual Result - Passed.
        """
        out = self._capture_prints(player_io.import_song, self.state, "")
        self.assertIn("[import] Usage: /import <path_to_file>", out)

    def test_import_song_file_not_found(self):
        """
        Expected Result - Prints "File not found" error for non-existent paths.
        Actual Result is: Passed.
        """
        with tempfile.TemporaryDirectory() as tmp:
            missing = Path(tmp) / "ASDASD.mp3"
            out = self._capture_prints(player_io.import_song, self.state, str(missing))
            self.assertIn("[import] Error: File not found.", out)