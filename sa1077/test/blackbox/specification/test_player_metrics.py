import unittest
from unittest.mock import MagicMock, patch, mock_open
import sys
import io
from music_player import player_metrics

# Mock Classes

class MockTrack:
    """Mock object for a track."""
    def __init__(self, path, display_name="Unknown Title"):
        self.path = path
        self.display_name = display_name

class MockState:
    """Mock object for PlayerState."""
    def __init__(self):
        self.liked_tracks = set()
        self.play_counts = {}
        self.library_tracks = []
        self.current_track = None