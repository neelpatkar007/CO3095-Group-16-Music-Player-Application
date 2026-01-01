import unittest
from unittest.mock import MagicMock, patch
from pathlib import Path
from music_player import library_search_scan
from music_player.player_state import PlayerState


# Mocks

class MockTrack:
    def __init__(self, path_str, title="Title", artist="Artist", duration=60):
        self.path = Path(path_str) if path_str else None
        self.title = title
        self.artist = artist
        self.duration_seconds = duration

class TestLibrarySearchScanBranch(unittest.TestCase):
    """
    White-Box Branch Tests for library_search_scan.py.
    Testing Tool: Python unittest + unittest.mock
    Test Technique: White-Box Branch Testing
    """
    def setUp(self):
        self.mock_state = MagicMock(spec=PlayerState)
        self.mock_state.library_tracks = []