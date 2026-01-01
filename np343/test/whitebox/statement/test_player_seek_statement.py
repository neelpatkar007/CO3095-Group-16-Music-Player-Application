import unittest
from unittest.mock import MagicMock, patch
from music_player import player_seek
from music_player.player_state import PlayerState
from music_player.library import Track

class TestPlayerSeekStatement(unittest.TestCase):
    """
    White-Box Statement Tests for player_seek.py.
    Testing Tool: Python unittest + unittest.mock
    Test Technique: White-Box Statement Testing
    """

    def setUp(self):
        self.state = MagicMock(spec=PlayerState)
        self.state.current_track = MagicMock(spec=Track)
        self.state.current_track.duration_seconds = 200.0
        self.state.position_seconds = 50.0
        self.state.audio_engine = MagicMock()