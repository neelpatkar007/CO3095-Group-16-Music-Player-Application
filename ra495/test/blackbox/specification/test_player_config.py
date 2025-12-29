import unittest
import json
from unittest.mock import MagicMock, patch, mock_open
from music_player import player_config
from music_player.player_state import PlayerState
from music_player.library import Track
from pathlib import Path


class TestPlayerConfig(unittest.TestCase):
    """
    Black-Box Specification-based Testing for player_config.py.
    Testing Tool: Python unittest + unittest.mock
    Test Technique: Category Partition Method using TSLGenerator
    Source: playerConfig.txt
    """

    def setUp(self):
        self.state = PlayerState([], MagicMock())
        # Setup dummy library for testing tags/stats
        self.track1 = Track(Path("a.mp3"), "Song A", "Artist A", 100)
        self.track2 = Track(Path("b.mp3"), "Song B", "Artist B", 200)
        self.state.library_tracks = [self.track1, self.track2]

    # Save/Load Settings Tests

    def test_save_settings_success(self):
        """
        Expected Result: JSON data is written to player_config.json.
        Actual Result: [config] Settings saved.
        """
        self.state.volume = 80
        self.state.shuffle_active = True

        with patch("builtins.open", mock_open()) as mocked_file:
            player_config.save_settings(self.state)
            mocked_file.assert_called_with(Path("player_config.json"), "w")
            handle = mocked_file()
            handle.write.assert_called()

    def test_load_settings_success(self):
        """
        Expected Result: State attributes are updated from file.
        Actual Result: [config] Settings loaded.
        """
        fake_json = json.dumps({"volume": 50, "shuffle": True})

        with patch("builtins.open", mock_open(read_data=fake_json)):
            with patch("pathlib.Path.exists", return_value=True):
                player_config.load_settings(self.state)

        self.assertEqual(self.state.volume, 50)
        self.assertTrue(self.state.shuffle_active)

    def test_load_settings_corrupt(self):
        """
        Expected Result: Error handled without crashing and defaults values are used instead.
        Actual Result: [config] Error loading settings: Expecting property name enclosed in double quotes: line 1 column 2 (char 1)
        """
        with patch("builtins.open", mock_open(read_data="{invalid_json")):
            with patch("pathlib.Path.exists", return_value=True):
                player_config.load_settings(self.state)

        self.assertEqual(self.state.volume, 100)