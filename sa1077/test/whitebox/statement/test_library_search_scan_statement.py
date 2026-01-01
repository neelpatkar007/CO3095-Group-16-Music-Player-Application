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

    def test_view_songs_table(self):
        """
        Expected Result: Prints all songs.
        Actual Result:
        PASSED [100%][lib] Songs (library):
         No  Title                           Artist                  Time
        -----------------------------------------------------------------
          1  Title                           Artist                 01:00
        """
        self.mock_state.library_tracks = [MockTrack("/a.mp3")]
        library_search_scan.view_songs_table(self.mock_state)

    def test_view_artists_table(self):
        """
        Expected Result: Groups by artist and prints artist table.
        Actual Result:
        Artist                     Tracks      Time
        ---------------------------------------------
        Artist X                        2     02:30
        Artist Y                        1     00:10

        """
        t1 = MockTrack("/a.mp3", artist="Artist X", duration=100)
        t2 = MockTrack("/b.mp3", artist="Artist X", duration=50)
        t3 = MockTrack("/c.mp3", artist="Artist Y", duration=10)
        self.mock_state.library_tracks = [t1, t2, t3]

        library_search_scan.view_artists_table(self.mock_state)

    def test_view_albums_table(self):
        """
        Expected Result: Groups by album and prints table.
        Actual Result:
        Album (folder)             Tracks      Time
        ---------------------------------------------
        Album A                         2     02:00
        """
        t1 = MockTrack("/Music/Album A/01.mp3", duration=60)
        t2 = MockTrack("/Music/Album A/02.mp3", duration=60)
        self.mock_state.library_tracks = [t1, t2]

        library_search_scan.view_albums_table(self.mock_state)

    @patch("music_player.library_search_scan.discover_tracks")
    def test_rescan_new_tracks_found(self, mock_discover):
        """
        Expected Result: Finds new tracks, adds them to library, and prints count.
        Actual Result:
        PASSED [100%][lib] Scanning for new tracks...
        [lib] Added 1 new track(s).
        """
        existing = MockTrack("/old.mp3")
        new_one = MockTrack("/new.mp3")

        self.mock_state.library_tracks = [existing]
        mock_discover.return_value = [existing, new_one]
        self.mock_state.tracks = self.mock_state.library_tracks
        library_search_scan.rescan_for_new_tracks(self.mock_state)

        self.assertIn(new_one, self.mock_state.library_tracks)


if __name__ == '__main__':
    unittest.main()