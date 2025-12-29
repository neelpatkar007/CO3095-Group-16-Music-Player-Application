import unittest
from unittest.mock import MagicMock, patch
from music_player import player_core
from music_player.player_state import PlayerState
from music_player.library import Track
from pathlib import Path


class TestPlayerCoreStatement(unittest.TestCase):
    """
    White-Box Statement Testing for player_core.py.
    Testing Tool: Python unittest + unittest.mock
    Test Technique: White-Box Statement Testing
    """

    def setUp(self):
        self.mock_engine = MagicMock()
        self.state = PlayerState([], self.mock_engine)
        self.sample_track = Track(Path("song.mp3"), "Test Song", "Artist", 180)

    # Play Tests

    def test_play_errors(self):
        """
        Expected Result: Handles None state and missing tracks without crashing.
        Actual Result:
            [core] Error: State is None.
            [core] No tracks loaded.
        """
        # Test None state
        player_core.play(None)

        # Test No Tracks
        self.state.tracks = []
        player_core.play(self.state)

