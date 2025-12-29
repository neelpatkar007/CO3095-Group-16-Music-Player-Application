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

    # Load Settings Tests

    def test_load_settings_none_state(self):
        """
        Expected Result: Returns early.
        Actual Result: [config] Error loading settings: 'NoneType' object has no attribute 'volume'
        """
        player_config.load_settings(None)

    def test_load_settings_no_file(self):
        """
        Expected Result: Returns early.
        Actual Result: Function returns.
        """
        with patch("pathlib.Path.exists", return_value=False):
            player_config.load_settings(self.state)

    def test_load_settings_success(self):
        """
        Expected Result: State updated and engine volume set.
        Actual Result: [config] Settings loaded.
        """
        fake_data = json.dumps({"volume": 80, "shuffle": True})
        with patch("pathlib.Path.exists", return_value=True):
            with patch("builtins.open", mock_open(read_data=fake_data)):
                player_config.load_settings(self.state)
        self.assertEqual(self.state.volume, 80)
        self.state.audio_engine.set_volume.assert_called_with(80)

    def test_load_settings_exception(self):
        """
        Expected Result: Prints error message.
        Actual Result: [config] Error loading settings: Expecting property name enclosed in double quotes: line 1 column 2 (char 1)
        """
        with patch("pathlib.Path.exists", return_value=True):
            with patch("builtins.open", mock_open(read_data="{bad_json")):
                player_config.load_settings(self.state)