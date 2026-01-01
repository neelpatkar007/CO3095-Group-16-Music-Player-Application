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


class MockPlaylist:
    def __init__(self, name, tracks=None):
        self.name = name
        self.tracks = tracks if tracks else []

# Test Class

class TestUserDataStatement(unittest.TestCase):

    """
    White-Box Statement Tests for user_data.py.
    Testing Tool: Python unittest + unittest.mock
    Test Technique: White-Box Statement Testing
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

    def test_helpers_serialize_none(self):
        """
        Expected Result: Returns an empty dictionary.
        Actual Result: Passed.
        """
        res = user_data._serialize_current_state(None)
        self.assertEqual(res, {})

    def test_helpers_save_profiles_error(self):
        """
        Expected Result: Catches the OSError/Exception and prints an error message.
        Actual Result: PASSED [100%][profile] Error saving: Disk full
        """
        with patch("builtins.open", mock_open()) as m:
            m.side_effect = OSError("Disk full")
            user_data._save_profiles(self.mock_state)

    def test_helpers_save_current_none(self):
        """
        Expected Result: Returns immediately without error when state is None.
        Actual Result: Passed.
        """
        user_data._save_current_to_profile(None)

    def test_helpers_apply_data_none_or_empty(self):
        """
        Expected Result: If state is None then returns and when data is empty liked_tracks set and playlists list empty.
        Actual Result: Passed.
        """
        # State None
        user_data._apply_profile_data(None, {})

        # Data Empty
        user_data._apply_profile_data(self.mock_state, {})
        self.assertEqual(self.mock_state.liked_tracks, set())
        self.assertEqual(self.mock_state.playlists, [])
