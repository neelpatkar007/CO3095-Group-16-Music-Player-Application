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