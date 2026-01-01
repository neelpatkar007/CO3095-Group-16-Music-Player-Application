import unittest
from unittest.mock import MagicMock, patch
from pathlib import Path
from music_player import library_search_scan
from music_player.player_state import PlayerState


class MockTrack:
    def __init__(self, path_str, title="Title", artist="Artist", duration=60):
        self.path = Path(path_str) if path_str else None
        self.title = title
        self.artist = artist
        self.duration_seconds = duration


class TestLibrarySearchScanStatement(unittest.TestCase):
    """
    White-Box Statement Tests for library_search_scan.py.
    Testing Tool: Python unittest + unittest.mock
    Test Technique: White-Box Statement Testing
    """

    def setUp(self):
        self.mock_state = MagicMock(spec=PlayerState)
        self.mock_state.library_tracks = []
        self.mock_state.tracks = []

    def test_print_tracks_table_basic(self):
        """
        Expected Result: Prints table header and one row.
        Actual Result:
        No  Title                           Artist                  Time
        -----------------------------------------------------------------
          1  Song A                          Artist A               02:00
        """
        tracks = [MockTrack("/a/b.mp3", "Song A", "Artist A", 120)]
        library_search_scan._print_tracks_table(tracks)

    def test_search_library_match(self):
        """
        Expected Result: Finds match and prints results table.
        Actual Result:
        [lib] Search results for 'love':
         No  Title                           Artist                  Time
        -----------------------------------------------------------------
          1  Love Song                       The Band               03:20
        """
        t1 = MockTrack("/music/song1.mp3", "Love Song", "The Band", 200)
        self.mock_state.library_tracks = [t1]
        library_search_scan.search_library(self.mock_state, "love")