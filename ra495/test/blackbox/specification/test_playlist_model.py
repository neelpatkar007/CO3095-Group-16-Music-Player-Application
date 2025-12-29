import unittest
from music_player.playlist_model import Playlist
from music_player.library import Track
from pathlib import Path


class TestPlaylistModel(unittest.TestCase):
    """
    Black-Box Specification-based Testing for playlist_model.py.
    Testing Tool: Python unittest
    Test Technique: Category Partition Method using TSLGenerator
    Source: playlistModel.txt
    """

    def setUp(self):
        self.t1 = Track(Path("1.mp3"), "T1", "A1", 60)
        self.t2 = Track(Path("2.mp3"), "T2", "A1", 90)

    # Initialisation Tests

    def test_init_valid(self):
        """
        Expected Result: Object created with correct name and empty track list.
        Actual Result: Name='My Mix', Tracks=[]
        """
        pl = Playlist("My Mix")
        self.assertEqual(pl.name, "My Mix")
        self.assertEqual(pl.tracks, [])

    def test_init_empty_name(self):
        """
        Expected Result: Name defaults to "(unnamed)".
        Actual Result: Name='(unnamed)'
        """
        pl = Playlist("")
        self.assertEqual(pl.name, "(unnamed)")

    # Duration Tests

    def test_total_duration_valid(self):
        """
        Expected Result: Sum of durations matches (60+90=150s).
        Actual Result: 150.0 seconds / 02:30
        """
        pl = Playlist("Mix", [self.t1, self.t2])
        self.assertEqual(pl.total_duration_seconds, 150.0)
        self.assertEqual(pl.total_duration_mm_ss, "02:30")

    def test_total_duration_mixed_invalid(self):
        """
        Expected Result: 'None' durations are treated as 0 and ignored.
        Actual Result: 60.0 seconds
        """
        t3 = Track(Path("3.mp3"), "T3", duration_seconds=None)
        pl = Playlist("Mix", [self.t1, t3])
        self.assertEqual(pl.total_duration_seconds, 60.0)