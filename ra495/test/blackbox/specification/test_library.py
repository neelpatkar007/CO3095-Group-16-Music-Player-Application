import unittest
from unittest.mock import MagicMock, patch
from pathlib import Path
from music_player import library
from music_player.library import Track


class TestLibrary(unittest.TestCase):
    """
    Black-Box Specification-based Testing for library.py.
    Testing Tool: Python unittest + unittest.mock
    Test Technique: Category Partition Method
    Source: mainTSL.txt
    """

    def setUp(self):
        # Patch the global MUSIC_DIR to point to a mock
        self.patcher = patch("music_player.library.MUSIC_DIR")
        self.mock_music_dir = self.patcher.start()

    def tearDown(self):
        self.patcher.stop()

    # Track Dataclass Tests

    def test_track_display_name_formatted(self):
        """
        Expected Result: Returns "Title – Artist" when both are present.
        Actual Result: Song A – Artist A
        """
        t = Track(Path("a.mp3"), "Song A", "Artist A", 180)
        self.assertEqual(t.display_name, "Song A – Artist A")

    def test_track_display_name_simple(self):
        """
        Expected Result: Returns only Title when Artist is empty.
        Actual Result: Song B
        """
        t = Track(Path("b.mp3"), "Song B", "", 180)
        self.assertEqual(t.display_name, "Song B")