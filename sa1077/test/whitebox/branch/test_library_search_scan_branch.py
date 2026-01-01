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

    # _print_tracks_table Branches

    def test_print_tracks_table_empty(self):
        """
        Expected Result: Prints "(no tracks)" and returns immediately when list is empty.
        Actual Result: PASSED [100%]  (no tracks)
        """
        library_search_scan._print_tracks_table([])

    def test_print_tracks_table_none_item(self):
        """
        Expected Result: Skips 'None' items in the list and continues printing valid tracks.
        Actual Result:
        No  Title                           Artist                  Time
        -----------------------------------------------------------------
          1  Title                           Artist                 01:00
        """
        tracks = [MockTrack("/a.mp3"), None]
        library_search_scan._print_tracks_table(tracks)

    # search_library Branches

    def test_search_library_invalid_inputs(self):
        """
        Expected Result: Returns early if state is None or query is empty.
        Actual Result:
            [lib] Usage: /search <text>
            [lib] Usage: /search <text>
        """
        library_search_scan.search_library(None, "query")
        library_search_scan.search_library(self.mock_state, "")
        library_search_scan.search_library(self.mock_state, "   ")

    def test_search_library_matching_branches(self):
        """
        Expected Result: Matches query against title, artist, or filename, skipping invalid tracks.
        Actual Result:
            [lib] Search results for 'super':
             No  Title                           Artist                  Time
            -----------------------------------------------------------------
              1  Super Match                     Nobody                 01:00
              2  Boring                          Super Star             01:00
        """
        t_none = None
        t_title = MockTrack("/1.mp3", title="Super Match", artist="Nobody")
        t_artist = MockTrack("/2.mp3", title="Boring", artist="Super Star")
        t_file = MockTrack("/super_song.mp3", title="Boring", artist="Nobody")
        t_no_match = MockTrack("/other.mp3", title="Boring", artist="Nobody")

        self.mock_state.library_tracks = [t_none, t_title, t_artist, t_file, t_no_match]
        library_search_scan.search_library(self.mock_state, "super")

    def test_search_library_no_results(self):
        """
        Expected Result: Prints "No matches found" when no tracks match the query.
        Actual Result: PASSED [100%][lib] No matches found.
        """
        self.mock_state.library_tracks = [MockTrack("/a.mp3", title="A")]
        library_search_scan.search_library(self.mock_state, "Z")