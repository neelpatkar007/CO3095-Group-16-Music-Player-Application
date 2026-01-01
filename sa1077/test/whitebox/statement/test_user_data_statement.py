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