import unittest
from unittest.mock import MagicMock, patch
from pathlib import Path
from music_player import library


class TestLibraryBranch(unittest.TestCase):
    """
    White-Box Branch Testing for library.py.
    Testing Tool: Python unittest + unittest.mock
    Test Technique: Branch Testing (White-Box)
    """

    def test_read_metadata_branches(self):
        """
        Branches:
         - if not HAS_MUTAGEN
         - if audio is None
         - if info is not None
         - if hasattr(info, "length")
         - if tags
         - if "TIT2" in tags
         - if "TPE1" in tags
        Expected Result: Returns defaults for missing data and correct values for valid tags.

        """
        path = Path("test.mp3")
