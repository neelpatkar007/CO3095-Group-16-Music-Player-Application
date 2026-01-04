import unittest
from unittest.mock import MagicMock, patch
from pathlib import Path
from music_player.library import _read_metadata


class TestConcolicExecution(unittest.TestCase):

    def setUp(self):
        self.path = Path("concolic.mp3")

    @patch("music_player.library.HAS_MUTAGEN", False)
    def test_iteration_1_initial_seed(self):
        """
        Iteration 1: Initial concrete seed is 'No Mutagen'.
        Constraint: NOT S2.
        """
        title, artist, duration = _read_metadata(self.path)
        self.assertEqual(title, "concolic")
        self.assertEqual(artist, "Unknown")
        self.assertIsNone(duration)

    @patch("music_player.library.HAS_MUTAGEN", True)
    @patch("music_player.library.mutagen.File")
    def test_iteration_2_flip_mutagen_check(self, mock_mutagen_file):
        """
        Iteration 2: We flip 'NOT S2' to 'S2'.
        New Path taken: S2 is True, but S3 (audio) is None.
        """
        mock_mutagen_file.return_value = None

        title, artist, duration = _read_metadata(self.path)

        self.assertEqual(title, "concolic")
        self.assertEqual(artist, "Unknown")
        self.assertIsNone(duration)

    @patch("music_player.library.HAS_MUTAGEN", True)
    @patch("music_player.library.mutagen.File")
    def test_iteration_3_flip_duration_constraint(self, mock_mutagen_file):
        """
        Iteration 3: We traverse deep into the function.
        We specifically flip the 'success' constraint of float conversion (S4).
        """
        mock_audio = MagicMock()
        mock_mutagen_file.return_value = mock_audio
        mock_audio.info.length = "invalid_float"
        mock_audio.tags = None

        title, artist, duration = _read_metadata(self.path)

        self.assertIsNone(duration)

    @patch("music_player.library.HAS_MUTAGEN", True)
    @patch("music_player.library.mutagen.File")
    def test_iteration_4_flip_tag_presence(self, mock_mutagen_file):
        """
        Iteration 4: Exploring the Tag logic.
        We flip the constraint that 'TIT2' exists in tags (S6).
        """
        mock_audio = MagicMock()
        mock_mutagen_file.return_value = mock_audio
        mock_audio.info.length = 100.0
        mock_audio.tags = {"TPE1": "Concolic Artist"}

        title, artist, duration = _read_metadata(self.path)

        self.assertEqual(title, "concolic")
        self.assertEqual(artist, "Concolic Artist")
        self.assertEqual(duration, 100.0)


if __name__ == "__main__":
    unittest.main()
