import unittest
from music_player.playlist_model import Playlist
from music_player.library import Track
from pathlib import Path


class TestPlaylistModelBranch(unittest.TestCase):
    """
    White-Box Branch Testing for playlist_model.py.
    Testing Tool: Python unittest
    Test Technique: Branch Coverage (White-Box)
    """

    def setUp(self):
        self.t1 = Track(Path("1.mp3"), "T1", "A1", 60)

    def test_init_branches(self):
        """
        Branches:
         - if name not str
         - name.strip() or fallback
         - if tracks is None / not list
        """
        # Name Type (True)
        p1 = Playlist(999)
        self.assertEqual(p1.name, "999")
        # Name Fallback (True)
        p2 = Playlist("   ")
        self.assertEqual(p2.name, "(unnamed)")

        # Tracks Validation
        # True (None)
        p3 = Playlist("A", None)
        self.assertEqual(p3.tracks, [])
        # Elif (Not List)
        p4 = Playlist("B", "NotList")
        self.assertEqual(p4.tracks, [])
        # Else (Valid)
        p5 = Playlist("C", [self.t1])
        self.assertEqual(len(p5.tracks), 1)

    def test_duration_branches(self):
        """
        Branches:
         - if tracks empty
         - if duration is a valid type and > 0
        """
        # Empty (True)
        p_empty = Playlist("E")
        self.assertEqual(p_empty.total_duration_mm_ss, "00:00")

        # Duration Validation (True/False/False)
        t_valid = Track(Path("a"), "A", duration_seconds=10)
        t_none = Track(Path("b"), "B", duration_seconds=None)
        t_zero = Track(Path("c"), "C", duration_seconds=0)

        p = Playlist("Mix", [t_valid, t_none, t_zero])
        self.assertEqual(p.total_duration_seconds, 10.0)