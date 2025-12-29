import unittest
import json
from unittest.mock import MagicMock, patch, mock_open
from music_player import player_config
from music_player.player_state import PlayerState
from music_player.library import Track
from pathlib import Path


class TestPlayerConfigStatement(unittest.TestCase):
    """
    White-Box Statement Testing for player_config.py.
    Testing Tool: Python unittest + unittest.mock
    Test Technique: Statement (White-Box)
    """

    def setUp(self):
        self.state = PlayerState([], MagicMock())
        self.state.audio_engine = MagicMock()
        self.track1 = Track(Path("a.mp3"), "Song A", "Artist A", 100)
        self.state.library_tracks = [self.track1]

    # Save Settings Tests

    def test_save_settings_none_state(self):
        """
        Expected Result: Returns early.
        Actual Result: Function returns.
        """
        player_config.save_settings(None)

    def test_save_settings_success(self):
        """
        Expected Result: Settings saved message.
        Actual Result: [config] Settings saved.
        """
        self.state.volume = 50
        with patch("builtins.open", mock_open()):
            player_config.save_settings(self.state)

    def test_save_settings_exception(self):
        """
        Expected Result: Prints error message.
        Actual Result: [config] Error saving settings: Denied
        """
        with patch("builtins.open", side_effect=PermissionError("Denied")):
            player_config.save_settings(self.state)