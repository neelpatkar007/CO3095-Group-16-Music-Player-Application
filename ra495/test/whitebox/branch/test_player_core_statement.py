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

    def test_play_execution_paths(self):
        """
        Expected Result: Covers Resume and Fresh Start logic.
        Actual Result:
            [core] Resumed: Test Song – Artist
            [core] Playing: Test Song – Artist (1.0x)
        """
        self.state.tracks = [self.sample_track]
        self.state.current_index = 0

        # Resume
        self.state.is_paused = True
        player_core.play(self.state)
        self.mock_engine.resume.assert_called()

        # Fresh Play
        self.state.is_paused = False
        self.state.is_playing = False
        player_core.play(self.state)
        self.mock_engine.play.assert_called()

    # Pause and Stop Tests

    def test_pause_stop_logic(self):
        """
        Expected Result: Pause and Stop update flags correctly.
        Actual Result:
            [core] Paused.
            [core] Stopped.
        """
        # Pause
        self.state.is_playing = True
        player_core.pause(self.state)
        self.assertTrue(self.state.is_paused)

        # Stop
        player_core.stop(self.state)
        self.assertEqual(self.state.position_seconds, 0.0)