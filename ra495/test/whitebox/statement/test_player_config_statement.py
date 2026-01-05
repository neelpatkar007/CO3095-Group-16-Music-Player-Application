import unittest
import json
from unittest.mock import MagicMock, patch, mock_open
from music_player import player_config
from music_player.player_state import PlayerState
from music_player.library import Track
from pathlib import Path


class TestPlayerConfigStatement(unittest.TestCase):


    def setUp(self):
        self.state = PlayerState([], MagicMock())
        self.state.audio_engine = MagicMock()
        self.track1 = Track(Path("a.mp3"), "Song A", "Artist A", 100)
        self.state.library_tracks = [self.track1]


    def test_save_settings_none_state(self):
        player_config.save_settings(None)

    def test_save_settings_success(self):
        self.state.volume = 50
        with patch("builtins.open", mock_open()):
            player_config.save_settings(self.state)

    def test_save_settings_exception(self):
        with patch("builtins.open", side_effect=PermissionError("Denied")):
            player_config.save_settings(self.state)


    def test_load_settings_none_state(self):
        player_config.load_settings(None)

    def test_load_settings_no_file(self):
        with patch("pathlib.Path.exists", return_value=False):
            player_config.load_settings(self.state)

    def test_load_settings_success(self):
        fake_data = json.dumps({"volume": 80, "shuffle": True})
        with patch("pathlib.Path.exists", return_value=True):
            with patch("builtins.open", mock_open(read_data=fake_data)):
                player_config.load_settings(self.state)
        self.assertEqual(self.state.volume, 80)
        self.state.audio_engine.set_volume.assert_called_with(80)

    def test_load_settings_exception(self):
        with patch("pathlib.Path.exists", return_value=True):
            with patch("builtins.open", mock_open(read_data="{bad_json")):
                player_config.load_settings(self.state)


    def test_add_tag_none_state(self):
        player_config.add_tag(None, "1", "tag")

    def test_add_tag_state_invalid_attrs(self):
        bad_state = MagicMock()
        del bad_state.library_tracks
        player_config.add_tag(bad_state, "1", "tag")

    def test_add_tag_index_none(self):
        player_config.add_tag(self.state, None, "tag")

    def test_add_tag_out_of_bounds(self):
        player_config.add_tag(self.state, "99", "tag")

    def test_add_tag_tag_none(self):
        player_config.add_tag(self.state, "1", None)

    def test_add_tag_track_missing(self):
        self.state.library_tracks = [None]
        player_config.add_tag(self.state, "1", "tag")

    def test_add_tag_init_dict(self):
        self.state.song_tags = {}
        player_config.add_tag(self.state, "1", "new")
        self.assertIn("new", self.state.song_tags[str(self.track1.path)])

    def test_add_tag_invalid_chars(self):
        player_config.add_tag(self.state, "1", "bad!")

    def test_add_tag_existing(self):
        path = str(self.track1.path)
        self.state.song_tags = {path: ["exists"]}
        player_config.add_tag(self.state, "1", "exists")


    def test_list_tags_none_state(self):
        player_config.list_all_tags(None)

    def test_list_tags_empty(self):
        self.state.song_tags = {}
        player_config.list_all_tags(self.state)

    def test_list_tags_populated(self):
        self.state.song_tags = {"song1": ["gym"]}
        player_config.list_all_tags(self.state)


    def test_filter_none_state(self):
        player_config.filter_by_tag(None, "tag")

    def test_filter_tag_none(self):
        player_config.filter_by_tag(self.state, None)

    def test_filter_no_matches(self):
        player_config.filter_by_tag(self.state, "gym")

    def test_filter_matches_found(self):
        path = str(self.track1.path)
        self.state.song_tags = {path: ["gym"]}
        player_config.filter_by_tag(self.state, "gym")
        self.assertEqual(len(self.state.tracks), 1)


    def test_stats_none_state(self):
        player_config.view_stats(None)

    def test_stats_missing_attr(self):
        del self.state.play_counts
        player_config.view_stats(self.state)

    def test_stats_empty_counts(self):
        self.state.play_counts = {}
        player_config.view_stats(self.state)

    def test_stats_populated(self):

        self.state.play_counts = {str(self.track1.path): 5}
        self.state.total_play_time = 3600
        player_config.view_stats(self.state)