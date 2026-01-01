import unittest
from unittest.mock import MagicMock, patch
from music_player import player_shortcuts
from music_player.player_state import PlayerState


class TestPlayerShortcutsSpec(unittest.TestCase):
    """
    Black-Box Specification Testing for player_shortcuts.py.
    Testing Tool: Python unittest + unittest.mock
    Test Technique: Black-Box Specification Testing
    """

    def setUp(self):
        self.state = MagicMock(spec=PlayerState)
        self.state.tracks = [MagicMock()]  # Ensure tracks exist by default
        self.state.is_playing = False
        self.state.volume = 50

    def test_handle_play_pause(self):
        """
        Expected Result:
         - 1. Prints - "Error: No tracks loaded" if library is empty.
         - 2. Calls pause() if playback is active.
         - 3.  play() if playback is stopped/ or paused.
        Actual Result: Passed. Verified function calls and print output.
        """
        # No tracks
        self.state.tracks = []
        with patch("builtins.print") as mock_print:
            player_shortcuts.handle_keypress(self.state, "p")
            mock_print.assert_called_with("[shortcuts] Error: No tracks loaded.")

        # Play
        self.state.tracks = [MagicMock()]
        self.state.is_playing = False
        with patch("music_player.player_core.play") as mock_play:
            player_shortcuts.handle_keypress(self.state, "p")
            mock_play.assert_called_once()

        # Pause
        self.state.is_playing = True
        with patch("music_player.player_core.pause") as mock_pause:
            player_shortcuts.handle_keypress(self.state, "p")
            mock_pause.assert_called_once()

    def test_handle_stop(self):
        """
        Expected Result : Calls stop() only if playback is currently active. If already stopped do nothing.
        Actual Result : Passed. Verified 'stop' is only called when is_playing is True.
        """
        # Playing to Stopped
        self.state.is_playing = True
        with patch("music_player.player_core.stop") as mock_stop:
            player_shortcuts.handle_keypress(self.state, "s")
            mock_stop.assert_called_once()

        # Stopped
        self.state.is_playing = False
        with patch("music_player.player_core.stop") as mock_stop:
            player_shortcuts.handle_keypress(self.state, "s")
            mock_stop.assert_not_called()