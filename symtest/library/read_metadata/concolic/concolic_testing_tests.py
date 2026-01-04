import unittest
from unittest.mock import MagicMock, patch
from pathlib import Path
from typing import Tuple


def _read_metadata(path: Path, has_mutagen: bool = True) -> Tuple[str, str, float | None]:
    """Read metadata from audio file."""
    title = path.stem
    artist = "Unknown"
    duration: float | None = None

    if not has_mutagen:
        return title, artist, duration

    try:
        import mutagen
        audio = mutagen.File(path)
    except Exception:
        return title, artist, duration

    if audio is None:
        return title, artist, duration

    info = getattr(audio, "info", None)
    if info is not None and hasattr(info, "length"):
        try:
            duration = float(info.length)
        except Exception:
            duration = None

    tags = getattr(audio, "tags", None)
    if tags:
        if "TIT2" in tags:
            try:
                title = str(tags["TIT2"])
            except Exception:
                pass
        if "TPE1" in tags:
            try:
                artist = str(tags["TPE1"])
            except Exception:
                pass

    return title, artist, duration


class TestConcolicExecution(unittest.TestCase):

    def setUp(self):
        self.path = Path("concolic.mp3")

    def test_iteration_1_initial_seed(self):
        """
        Iteration 1: Initial concrete seed is 'No Mutagen'.
        Constraint: NOT S2.
        """
        title, artist, duration = _read_metadata(self.path, has_mutagen=False)
        self.assertEqual(title, "concolic")
        self.assertEqual(artist, "Unknown")
        self.assertIsNone(duration)

    @patch('mutagen.File')
    def test_iteration_2_flip_mutagen_check(self, mock_mutagen_file):
        """
        Iteration 2: We flip 'NOT S2' to 'S2'.
        New Path taken: S2 is True, but S3 (audio) is None.
        """
        mock_mutagen_file.return_value = None

        title, artist, duration = _read_metadata(self.path, has_mutagen=True)

        self.assertEqual(title, "concolic")
        self.assertEqual(artist, "Unknown")
        self.assertIsNone(duration)

    @patch('mutagen.File')
    def test_iteration_3_flip_duration_constraint(self, mock_mutagen_file):
        """
        Iteration 3: We traverse deep into the function.
        We specifically flip the 'success' constraint of float conversion (S4).
        """
        mock_audio = MagicMock()
        mock_mutagen_file.return_value = mock_audio
        mock_audio.info.length = "invalid_float"
        mock_audio.tags = None

        title, artist, duration = _read_metadata(self.path, has_mutagen=True)

        self.assertIsNone(duration)

    @patch('mutagen.File')
    def test_iteration_4_flip_tag_presence(self, mock_mutagen_file):
        """
        Iteration 4: Exploring the Tag logic.
        We flip the constraint that 'TIT2' exists in tags (S6).
        """
        mock_audio = MagicMock()
        mock_mutagen_file.return_value = mock_audio
        mock_audio.info.length = 100.0
        mock_audio.tags = {"TPE1": "Concolic Artist"}

        title, artist, duration = _read_metadata(self.path, has_mutagen=True)

        self.assertEqual(title, "concolic")
        self.assertEqual(artist, "Concolic Artist")
        self.assertEqual(duration, 100.0)


if __name__ == "__main__":
    unittest.main()