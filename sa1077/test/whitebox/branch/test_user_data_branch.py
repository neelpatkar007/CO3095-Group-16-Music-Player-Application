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