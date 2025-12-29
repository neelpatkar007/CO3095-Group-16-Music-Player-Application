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