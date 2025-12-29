import unittest
import json
from unittest.mock import MagicMock, patch, mock_open
from music_player import player_config
from music_player.player_state import PlayerState
from music_player.library import Track
from pathlib import Path


class TestPlayerConfig(unittest.TestCase):
    """
    Black-Box Specification-based Testing for player_config.py.
    Testing Tool: Python unittest + unittest.mock
    Test Technique: Category Partition Method using TSLGenerator
    Source: playerConfig.txt
    """

    def setUp(self):
        self.state = PlayerState([], MagicMock())
        # Setup dummy library for testing tags/stats
        self.track1 = Track(Path("a.mp3"), "Song A", "Artist A", 100)
        self.track2 = Track(Path("b.mp3"), "Song B", "Artist B", 200)
        self.state.library_tracks = [self.track1, self.track2]