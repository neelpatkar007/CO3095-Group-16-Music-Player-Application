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