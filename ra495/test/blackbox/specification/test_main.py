import unittest
from unittest.mock import MagicMock, patch
import threading
import time
from music_player import main
from music_player.player_state import PlayerState


class TestMain(unittest.TestCase):
    """
    Black-Box Specification-based Testing for main.py.
    Testing Tool: Python unittest + unittest.mock
    Test Technique: Category Partition Method
    Source: mainTSL.txt
    """

    def setUp(self):
        # Mock state and engine
        self.mock_engine = MagicMock()
        self.state = PlayerState([], self.mock_engine)

        # Default state values
        self.state.resume_active = False
        self.state.position_seconds = 0.0
        # Tracks list is empty by default

    # Core Command Handling

    def test_handle_command_empty(self):
        """
        Expected Result: Returns True.
        Actual Result: Input ignored.
        """
        result = main.handle_command(self.state, "   ")
        self.assertTrue(result)

    def test_handle_command_quit(self):
        """
        Expected Result: Returns False and saves metrics.
        Actual Result: Quit command processed.
        """
        with patch("music_player.player_metrics.save_data") as mock_save:
            result = main.handle_command(self.state, "/quit")
            self.assertFalse(result)
            mock_save.assert_called_once()

    def test_handle_command_shortcuts(self):
        """
        Expected Result: Single letters 'p', 's', 'm' dispatch to player_shortcuts.
        Actual Result: Shortcut handler called.
        """
        with patch("music_player.player_shortcuts.handle_keypress") as mock_key:
            main.handle_command(self.state, "p")
            mock_key.assert_called_with(self.state, "p")

    # Sprint 1 Tests (Playback)

    def test_command_play_fresh(self):
        """
        Expected Result: /play calls player_core.play() directly when no resume state exists.
        Actual Result: Core Play called.
        """
        self.state.resume_active = False

        with patch("music_player.player_core.play") as mock_play:
            main.handle_command(self.state, "/play")
            mock_play.assert_called_with(self.state)

    def test_command_play_resume(self):
        """
        Expected Result: /play triggers Seek logic if resume is active and track exists.
        Actual Result: [resume] Seeking to saved position: 45s...
        """
        self.state.resume_active = True
        self.state.position_seconds = 45.0

        # Add a dummy track so state.current_track is valid
        self.state.tracks = [MagicMock()]
        self.state.current_index = 0

        with patch("music_player.player_core.play") as mock_play, \
                patch("music_player.player_seek.seek_to") as mock_seek:
            main.handle_command(self.state, "/play")

            # Verify Resume Logic sequence
            mock_play.assert_called()
            mock_seek.assert_called_with(self.state, "45.0")
            self.assertFalse(self.state.resume_active)

    def test_command_seek_args(self):
        """
        Expected Result: /seek command passes arguments correctly to player_seek.
        Actual Result: Seek to 1:30.
        """
        with patch("music_player.player_seek.seek_to") as mock_seek:
            main.handle_command(self.state, "/seek 1:30")
            mock_seek.assert_called_with(self.state, "1:30")

    def test_command_seek_missing_args(self):
        """
        Expected Result: Prints usage error if arg missing, does not call seek.
        Actual Result: [main] Usage: /seek <mm:ss or seconds>
        """
        with patch("music_player.player_seek.seek_to") as mock_seek:
            main.handle_command(self.state, "/seek")
            mock_seek.assert_not_called()