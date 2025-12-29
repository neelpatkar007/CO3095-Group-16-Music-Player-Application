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

