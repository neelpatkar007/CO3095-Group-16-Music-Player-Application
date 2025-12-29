import unittest
from unittest.mock import MagicMock, patch
from music_player import player_core
from music_player.player_state import PlayerState
from music_player.library import Track
from pathlib import Path


class TestPlayerCore(unittest.TestCase):
    """
    Black-Box Specification-based Testing for player_core.py.

    Testing Tool: Python unittest + unittest.mock
    Test Technique: Category Partition Method using TSLGenerator
    """

    def setUp(self):
        # Mock of AudioEngine to simulate the real hardware behaviour
        self.mock_engine = MagicMock()
        self.state = PlayerState([], self.mock_engine)
        self.sample_track = Track(Path("song.mp3"), "Test Song", "Artist", 180)