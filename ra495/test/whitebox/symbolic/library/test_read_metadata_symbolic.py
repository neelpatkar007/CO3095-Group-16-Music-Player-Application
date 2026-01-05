import unittest
from unittest.mock import MagicMock, patch
from pathlib import Path
from music_player.library import _read_metadata


class TestSymbolicExecution(unittest.TestCase):


    def setUp(self):
        self.path = Path("song.mp3")

    @patch("music_player.library.HAS_MUTAGEN", False)
    def test_PC_1_no_library(self):

        title, artist, duration = _read_metadata(self.path)
        self.assertEqual(title, "song")
        self.assertEqual(artist, "Unknown")
        self.assertIsNone(duration)

    @patch("music_player.library.HAS_MUTAGEN", True)
    @patch("music_player.library.mutagen.File")
    def test_PC_2_load_failure(self, mock_mutagen_file):

        mock_mutagen_file.return_value = None

        title, artist, duration = _read_metadata(self.path)
        self.assertEqual(title, "song")
        self.assertEqual(artist, "Unknown")
        self.assertIsNone(duration)

    @patch("music_player.library.HAS_MUTAGEN", True)
    @patch("music_player.library.mutagen.File")
    def test_PC_3_valid_duration_no_tags(self, mock_mutagen_file):

        mock_audio = MagicMock()
        mock_mutagen_file.return_value = mock_audio
        mock_audio.info.length = 120.5
        mock_audio.tags = None

        title, artist, duration = _read_metadata(self.path)
        self.assertEqual(duration, 120.5)
        self.assertEqual(title, "song")
        self.assertEqual(artist, "Unknown")

    @patch("music_player.library.HAS_MUTAGEN", True)
    @patch("music_player.library.mutagen.File")
    def test_PC_4_maximal_success(self, mock_mutagen_file):

        mock_audio = MagicMock()
        mock_mutagen_file.return_value = mock_audio
        mock_audio.info.length = 300.0
        mock_audio.tags = {
            "TIT2": "Symbolic Song",
            "TPE1": "The Logic Gates"
        }

        title, artist, duration = _read_metadata(self.path)
        self.assertEqual(duration, 300.0)
        self.assertEqual(title, "Symbolic Song")
        self.assertEqual(artist, "The Logic Gates")

    @patch("music_player.library.HAS_MUTAGEN", True)
    @patch("music_player.library.mutagen.File")
    def test_PC_5_internal_exceptions(self, mock_mutagen_file):

        mock_audio = MagicMock()
        mock_mutagen_file.return_value = mock_audio
        mock_audio.info.length = "not_a_number"

        class BrokenTag:
            def __str__(self):
                raise ValueError("Tag Corrupt")

        mock_audio.tags = {
            "TIT2": BrokenTag(),
            "TPE1": BrokenTag()
        }

        title, artist, duration = _read_metadata(self.path)
        self.assertIsNone(duration)
        self.assertEqual(title, "song")
        self.assertEqual(artist, "Unknown")


if __name__ == "__main__":
    unittest.main()
