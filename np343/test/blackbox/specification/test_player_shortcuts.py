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

    def test_handle_volume_up(self):
        """
        Expected Result : Increases volume by 10 points. If volume would exceed 100, then it clamps to 100.
        Actual Result : PASSED [100%][shortcuts] Volume up: 100%
        """
        # Normal increment
        self.state.volume = 50
        with patch("builtins.print") as mock_print:
            player_shortcuts.handle_keypress(self.state, "+")
            self.assertEqual(self.state.volume, 60)
            # Verify print confirms new volume
            args = mock_print.call_args[0][0]
            self.assertIn("60%", args)

        # Cap at a 100
        self.state.volume = 95
        player_shortcuts.handle_keypress(self.state, "+")
        self.assertEqual(self.state.volume, 100)

        # Already Max -  Loop
        self.state.volume = 100
        player_shortcuts.handle_keypress(self.state, "+")
        self.assertEqual(self.state.volume, 100)

    def test_handle_volume_down(self):
        """
        Expected Result: Decreases volume by 10 points. If volume would drop below 0 then clamps to 0.
        Actual Result: PASSED [100%][shortcuts] Volume down: 0%
        """
        # Normal decrement
        self.state.volume = 50
        with patch("builtins.print") as mock_print:
            player_shortcuts.handle_keypress(self.state, "-")
            self.assertEqual(self.state.volume, 40)
            args = mock_print.call_args[0][0]
            self.assertIn("40%", args)

        # Clamp at 0
        self.state.volume = 5
        player_shortcuts.handle_keypress(self.state, "-")
        self.assertEqual(self.state.volume, 0)

        # Already Min
        self.state.volume = 0
        player_shortcuts.handle_keypress(self.state, "-")
        self.assertEqual(self.state.volume, 0)