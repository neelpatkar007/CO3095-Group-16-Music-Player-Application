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