import unittest
from unittest.mock import MagicMock, patch
import io
import sys
from music_player import player_ui
from music_player.player_state import PlayerState
from music_player.library import Track

class TestPlayerUISpec(unittest.TestCase):
    """
    Black-Box Specification Tests for player_ui.py.
    Testing Tool: Python unittest + unittest.mock + sys + io.
    Test Technique: Black-Box Specification Testing
    Source: playerUI.txt TSL Generated Test Frames
    """
    def setUp(self):
        self.captured_output = io.StringIO()
        self.sys_stdout = sys.stdout
        sys.stdout = self.captured_output
        self.mock_state = MagicMock(spec=PlayerState)
        self.mock_state.current_track = MagicMock(spec=Track)
        self.mock_state.current_track.display_name = "Song"
        self.mock_state.current_track.duration_seconds = 60

    def tearDown(self):
        sys.stdout = self.sys_stdout

    def get_output(self):
        return self.captured_output.getvalue().strip()
