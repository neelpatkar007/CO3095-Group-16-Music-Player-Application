import unittest
import json
from unittest.mock import MagicMock, patch, mock_open
from music_player import player_config
from music_player.player_state import PlayerState
from music_player.library import Track
from pathlib import Path


class TestPlayerConfigStatement(unittest.TestCase):
    """
    White-Box Statement Testing for player_config.py.
    Testing Tool: Python unittest + unittest.mock
    Test Technique: Statement (White-Box)
    """

    def setUp(self):
        self.state = PlayerState([], MagicMock())
        self.state.audio_engine = MagicMock()
        self.track1 = Track(Path("a.mp3"), "Song A", "Artist A", 100)
        self.state.library_tracks = [self.track1]