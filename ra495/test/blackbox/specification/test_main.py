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