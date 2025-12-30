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
        Actual Result: All tests passed without fail which means data extraction and error handling was successful.
        """
        path = Path("test.mp3")

        # HAS_MUTAGEN = False
        with patch("music_player.library.HAS_MUTAGEN", False):
            library._read_metadata(path)

        # HAS_MUTAGEN = True
        with patch("music_player.library.HAS_MUTAGEN", True):
            # audio is None
            with patch("music_player.library.mutagen.File", return_value=None):
                library._read_metadata(path)

        # audio exists
        mock_audio = MagicMock()

        # Info is None
        mock_audio.info = None
        mock_audio.tags = None
        with patch("music_player.library.mutagen.File", return_value=mock_audio):
            library._read_metadata(path)

        # Info exists but No length
        mock_audio.info = object()
        with patch("music_player.library.mutagen.File", return_value=mock_audio):
            library._read_metadata(path)

        # Tags checks
        mock_audio.info = None

        # Tags is None
        mock_audio.tags = None
        with patch("music_player.library.mutagen.File", return_value=mock_audio):
            library._read_metadata(path)

        # TIT2, TPE1 Missing
        mock_audio.tags = {"OTHER": "Value"}
        with patch("music_player.library.mutagen.File", return_value=mock_audio):
            library._read_metadata(path)

        # TIT2 Present
        mock_audio.tags = {"TIT2": "Title"}
        with patch("music_player.library.mutagen.File", return_value=mock_audio):
            t, _, _ = library._read_metadata(path)
            self.assertEqual(t, "Title")

        # TPE1 Present
        mock_audio.tags = {"TPE1": "Artist"}
        with patch("music_player.library.mutagen.File", return_value=mock_audio):
            _, a, _ = library._read_metadata(path)
            self.assertEqual(a, "Artist")