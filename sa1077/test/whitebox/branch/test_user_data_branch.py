import unittest
from unittest.mock import MagicMock, patch, mock_open
from music_player import user_data
from music_player.player_state import PlayerState

# Mocks

class MockTrack:
    def __init__(self, path, artist="Unknown", title="Unknown", duration=0):
        self.path = path
        self.artist = artist
        self.title = title
        self.duration_seconds = duration
        self.display_name = title


class TestUserDataBranch(unittest.TestCase):
    """
    White-Box Branch Tests for user_data.py.
    Testing Tool: Python unittest + unittest.mock
    Test Technique: White-Box Branch Testing
    """

    def setUp(self):
        self.mock_state = MagicMock(spec=PlayerState)
        self.mock_state.profiles = {}
        self.mock_state.active_profile = "default"
        self.mock_state.playlists = []
        self.mock_state.liked_tracks = set()
        self.mock_state.song_ratings = {}
        self.mock_state.library_tracks = []
        self.mock_state.current_track = None

    # create_profile

    def test_create_profile_branches(self):
        # State Invalid
        user_data.create_profile(None, "valid")

        # Name Invalid
        user_data.create_profile(self.mock_state, "")

        # Name == default
        user_data.create_profile(self.mock_state, "default")

        # Name exists
        self.mock_state.profiles = {"exists": {}}
        user_data.create_profile(self.mock_state, "exists")

        # Success
        with patch("music_player.user_data._save_profiles"):
            user_data.create_profile(self.mock_state, "new_one")
            self.assertIn("new_one", self.mock_state.profiles)

    # advanced_search

    @patch("music_player.time_utils.parse_timecode", return_value=60)
    @patch("music_player.time_utils.format_mm_ss", return_value="01:00")
    def test_advanced_search_branches(self, mock_fmt, mock_parse):
        t1 = MockTrack("/p1", artist="ArtistA", title="TitleA", duration=120)
        t2 = MockTrack("/p2", artist="ArtistB", title="TitleB", duration=30)
        self.mock_state.library_tracks = [t1, t2]

        # Artist
        user_data.advanced_search(self.mock_state, "artist:ArtistA")

        # Duration >
        user_data.advanced_search(self.mock_state, "duration>0:59")

        # Duration <
        user_data.advanced_search(self.mock_state, "duration<0:59")

        # Normal
        user_data.advanced_search(self.mock_state, "TitleB")

        # No matches
        with patch("builtins.print") as mock_print:
            user_data.advanced_search(self.mock_state, "NonExistentThing")
            mock_print.assert_any_call("[search] No matches found.")

    # rate_song

    def test_rate_song_branches(self):
        # No track
        self.mock_state.current_track = None
        user_data.rate_song(self.mock_state, "5")

        # Set valid track
        self.mock_state.current_track = MockTrack("/path")

        # Rating out of bounds
        user_data.rate_song(self.mock_state, "0")
        user_data.rate_song(self.mock_state, "6")

        # Invalid type
        user_data.rate_song(self.mock_state, "five")

        # Success Branch
        with patch("music_player.user_data._save_current_to_profile"):
            user_data.rate_song(self.mock_state, "5")
            self.assertEqual(self.mock_state.song_ratings["/path"], 5)

    # switch_profile

    def test_switch_profile_branches(self):
        self.mock_state.profiles = {"other": {"liked": []}}
        self.mock_state.active_profile = "default"

        # Does not exist
        user_data.switch_profile(self.mock_state, "missing")

        # Already active
        user_data.switch_profile(self.mock_state, "default")

        # Switch success
        with patch("music_player.user_data._save_profiles"):
            user_data.switch_profile(self.mock_state, "other")
            self.assertEqual(self.mock_state.active_profile, "other")


if __name__ == '__main__':
    unittest.main()
