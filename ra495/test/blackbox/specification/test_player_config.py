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

    # Custom Tag Tests

    def test_add_tag_valid(self):
        """
        Expected Result: Tag is appended to the song_tags dictionary for the correct track.
        Actual Result: [tags] Added #chill to 'Song A'.
        """
        player_config.add_tag(self.state, "1", "chill")

        tags = self.state.song_tags.get(str(self.track1.path))
        self.assertIn("chill", tags)

    def test_add_tag_duplicate(self):
        """
        Expected Result: Duplicate tag is ignored.
        Actual Result: [tags] Song already has tag #chill.
        """
        player_config.add_tag(self.state, "1", "chill")
        player_config.add_tag(self.state, "1", "chill")

        tags = self.state.song_tags.get(str(self.track1.path))
        self.assertEqual(tags.count("chill"), 1)

    def test_add_tag_invalid_index(self):
        """
        Expected Result: Error printed and no tags added.
        Actual Result: [tags] Error: Song index out of range.
        """
        player_config.add_tag(self.state, "99", "chill")
        self.assertEqual(len(self.state.song_tags), 0)

    def test_filter_by_tag_matches(self):
        """
        Expected Result: Playlist queue is replaced with matching tracks.
        Actual Result: [tags] Queue updated! Ready to play 1 songs tagged #gym.
        """
        self.state.song_tags[str(self.track2.path)] = ["gym"]

        player_config.filter_by_tag(self.state, "gym")

        self.assertEqual(len(self.state.tracks), 1)
        self.assertEqual(self.state.tracks[0], self.track2)

    def test_filter_by_tag_no_matches(self):
        """
        Expected Result: Queue remains unchanged (or empty handled gracefully).
        Actual Result: [tags] No songs found with #nonexistent.
        """
        player_config.filter_by_tag(self.state, "nonexistent")
        self.assertEqual(len(self.state.tracks), 0)

    # Playback Stats Tests

    def test_view_stats_populated(self):
        """
        Expected Result: Function runs successfully and prints stats.
        Actual Result:
            --- Playback Statistics ---
            Total Listening Time: 1h 0m
            Total Songs Played: 5
            Top Artists:
                Artist A: 5 plays
        """
        self.state.play_counts = {str(self.track1.path): 5}
        self.state.total_play_time = 3605

        player_config.view_stats(self.state)

    def test_view_stats_empty(self):
        """
        Expected Result: Function handles empty dict without crashing.
        Actual Result: [stats] No play history yet.
        """
        self.state.play_counts = {}
        player_config.view_stats(self.state)