import unittest
from unittest.mock import MagicMock, patch
from music_player import player_config
from music_player.player_state import PlayerState
from music_player.library import Track
from pathlib import Path


class TestPlayerConfigBranch(unittest.TestCase):
    """
    White-Box Branch Testing for player_config.py.
    Testing Tool: Python unittest + unittest.mock
    Test Technique: Branch Testing (White-Box)
    """

    def setUp(self):
        self.state = PlayerState([], MagicMock())
        self.track1 = Track(Path("a.mp3"), "Song A", "Artist A", 100)
        self.state.library_tracks = [self.track1]