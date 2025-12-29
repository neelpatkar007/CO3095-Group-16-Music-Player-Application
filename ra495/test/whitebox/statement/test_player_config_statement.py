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

    # Add Tag Tests

    def test_add_tag_none_state(self):
        """
        Expected Result: Prints Error.
        Actual Result: [tags] Error: State is None.
        """
        player_config.add_tag(None, "1", "tag")

    def test_add_tag_state_invalid_attrs(self):
        """
        Expected Result: Prints Corrupted Error.
        Actual Result: [tags] Error: Tag data is unavailable/corrupted.
        """
        bad_state = MagicMock()
        del bad_state.library_tracks
        player_config.add_tag(bad_state, "1", "tag")

    def test_add_tag_index_none(self):
        """
        Expected Result: Prints invalid format error.
        Actual Result: [tags] Error: Invalid number format.
        """
        player_config.add_tag(self.state, None, "tag")

    def test_add_tag_out_of_bounds(self):
        """
        Expected Result: Prints out of range error.
        Actual Result: [tags] Error: Song index out of range.
        """
        player_config.add_tag(self.state, "99", "tag")

    def test_add_tag_tag_none(self):
        """
        Expected Result: Prints error.
        Actual Result: [tags] Error: Tag cannot be empty.
        """
        player_config.add_tag(self.state, "1", None)

    def test_add_tag_track_missing(self):
        """
        Expected Result: Returns early.
        Actual Result: Function returns.
        """
        self.state.library_tracks = [None]
        player_config.add_tag(self.state, "1", "tag")

    def test_add_tag_init_dict(self):
        """
        Expected Result: Creates list for new song.
        Actual Result: [tags] Added #new to 'Song A'.
        """
        self.state.song_tags = {}
        player_config.add_tag(self.state, "1", "new")
        self.assertIn("new", self.state.song_tags[str(self.track1.path)])

    def test_add_tag_invalid_chars(self):
        """
        Expected Result: Prints invalid char error.
        Actual Result: [tags] Error: Invalid character '!'. Use A-Z, 0-9, _ only.
        """
        player_config.add_tag(self.state, "1", "bad!")

    def test_add_tag_existing(self):
        """
        Expected Result: Prints duplicate message.
        Actual Result: [tags] Song already has tag #exists.
        """
        path = str(self.track1.path)
        self.state.song_tags = {path: ["exists"]}
        player_config.add_tag(self.state, "1", "exists")

    # List Tags Tests

    def test_list_tags_none_state(self):
        """
        Expected Result: Prints Error.
        Actual Result: [tags] Error: State is None.
        """
        player_config.list_all_tags(None)

    def test_list_tags_empty(self):
        """
        Expected Result: Prints no tags message.
        Actual Result: [tags] No tags created yet.
        """
        self.state.song_tags = {}
        player_config.list_all_tags(self.state)

    def test_list_tags_populated(self):
        """
        Expected Result: Prints tags.
        Actual Result:
            --- Custom Tags ---
            #gym (1 songs)
        """
        self.state.song_tags = {"song1": ["gym"]}
        player_config.list_all_tags(self.state)

    # Filter By Tag Tests

    def test_filter_none_state(self):
        """
        Expected Result: Prints Error.
        Actual Result: [tags] Error: State is None.
        """
        player_config.filter_by_tag(None, "tag")

    def test_filter_tag_none(self):
        """
        Expected Result: Prints error.
        Actual Result: [tags] Error: Tag cannot be empty.
        """
        player_config.filter_by_tag(self.state, None)

    def test_filter_no_matches(self):
        """
        Expected Result: Prints no matches found.
        Actual Result: [tags] No songs found with #gym.
        """
        player_config.filter_by_tag(self.state, "gym")

    def test_filter_matches_found(self):
        """
        Expected Result: Updates state.tracks.
        Actual Result:
            [tags] Queue updated! Ready to play 1 songs tagged #gym:
            - Song A – Artist A
        """
        path = str(self.track1.path)
        self.state.song_tags = {path: ["gym"]}
        player_config.filter_by_tag(self.state, "gym")
        self.assertEqual(len(self.state.tracks), 1)

    # View Stats Tests

    def test_stats_none_state(self):
        """
        Expected Result: Prints error.
        Actual Result: [stats] Error: State is None.
        """
        player_config.view_stats(None)

    def test_stats_missing_attr(self):
        """
        Expected Result: Prints corrupted data error.
        Actual Result: [stats] Error: Play count data is corrupted.
        """
        del self.state.play_counts
        player_config.view_stats(self.state)

    def test_stats_empty_counts(self):
        """
        Expected Result: Prints no history.
        Actual Result: [stats] No play history yet.
        """
        self.state.play_counts = {}
        player_config.view_stats(self.state)

    def test_stats_populated(self):
        """
        Expected Result: Prints stats table.
        Actual Result:
            --- Playback Statistics ---
            Total Listening Time: 1h 0m
            Total Songs Played: 5

            Top Artists:
                Artist A: 5 plays
        """
        self.state.play_counts = {str(self.track1.path): 5}
        self.state.total_play_time = 3600
        player_config.view_stats(self.state)