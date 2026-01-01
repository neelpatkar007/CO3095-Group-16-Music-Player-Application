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

    def test_get_progress_exception(self):
        """
        Expected Result: Returns (0.0, None) when accessing state.current_track fails.
        Actual Result: Passed.
        """

        # Force exception when accessing - current_track
        class BrokenState:
            @property
            def current_track(self):
                raise AttributeError("Access failed")

        broken_state = BrokenState()
        pos, duration = player_seek.get_progress(broken_state)

        self.assertEqual(pos, 0.0)
        self.assertIsNone(duration)
