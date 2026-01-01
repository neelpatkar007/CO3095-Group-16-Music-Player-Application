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

    def test_render_progress_null_time(self):
        """
        Expected Result: Returns "[Time null]" string.
        Actual Result: Passed.
        """
        self.state.current_track.duration_seconds = None
        res = player_seek.render_progress_bar(self.state)
        self.assertEqual(res, "[Time null]")

    def test_nudge_state_none(self):
        """
        Expected Result: Returns None immediately.
        Actual Result: Passed.
        """
        player_seek.nudge(None, 5.0)

    def test_nudge_pos_invalid(self):
        """
        Expected Result: Defaults position to 0.0 and proceeds to seek.
        Actual Result: Passed.
        """
        self.state.position_seconds = "invalid"  # Force invalid type

        # Should default to 5.0
        player_seek.nudge(self.state, 5.0)

        # Verify seek called with 5.0
        self.state.audio_engine.seek.assert_called_with(5.0)

    def test_seek_to_state_none(self):
        """
        Expected Result: Returns None immediately.
        Actual Result: Passed.
        """
        player_seek.seek_to(None, 10.0)

    def test_seek_to_track_access_error(self):
        """
        Expected Result: Prints error message and returns.
        Actual Result: Passed.
        """

        class BrokenState:
            @property
            def current_track(self):
                raise TypeError("Bad type")

        broken_state = BrokenState()

        with patch("builtins.print") as mock_print:
            player_seek.seek_to(broken_state, 10.0)
            mock_print.assert_called_with("[seek] Error accessing track state.")

    def test_seek_to_engine_missing(self):
        """
        Expected Result: Updates state position but doesn't crash when calling .seek().
        Actual Result: Passed.
        """
        empty_state = MagicMock(spec=object)
        empty_state.current_track = MagicMock(spec=Track)
        empty_state.current_track.duration_seconds = 200.0

        player_seek.seek_to(empty_state, 10.0)
