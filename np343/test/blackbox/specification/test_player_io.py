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

    def test_import_song_source_is_directory(self):
        """
        Expected Result : Prints error if source path points to a directory instead of a file.
        Actual Result : Passed.
        """
        with tempfile.TemporaryDirectory() as tmp:
            src_dir = Path(tmp) / "folder"
            src_dir.mkdir()
            out = self._capture_prints(player_io.import_song, self.state, str(src_dir))
            self.assertIn("[import] Error: Source is not a file.", out)

    def test_import_song_empty_file_rejected(self):
        """
        Expected Result : Prints error if the source file is empty.
        Actual Result : Passed.
        """
        with tempfile.TemporaryDirectory() as tmp:
            supported_ext = next(iter(player_io.SUPPORTED_EXTENSIONS))
            src = Path(tmp) / f"empty{supported_ext}"
            src.write_bytes(b"")

            out = self._capture_prints(player_io.import_song, self.state, str(src))
            self.assertIn("[import] Error: File is empty.", out)