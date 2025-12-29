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

    # Discover Tracks Tests

    def test_discover_dir_missing(self):
        """
        Expected Result: Returns empty list and prints warning if MUSIC_DIR missing.
        Actual Result: [library] WARNING: MUSIC_DIR '<MagicMock name='MUSIC_DIR' id='1469366610496'>' does not exist.
        """
        self.mock_music_dir.exists.return_value = False
        tracks = library.discover_tracks()
        self.assertEqual(tracks, [])

    def test_discover_empty_dir(self):
        """
        Expected Result: Returns empty list if directory has no files.
        Actual Result: []
        """
        self.mock_music_dir.exists.return_value = True
        self.mock_music_dir.iterdir.return_value = []
        tracks = library.discover_tracks()
        self.assertEqual(tracks, [])

    def test_discover_ignored_extensions(self):
        """
        Expected Result: Skips files not in supported extensions list.
        Actual Result: Ignored 'image.jpg'.
        """
        self.mock_music_dir.exists.return_value = True

        fake_file = MagicMock()
        fake_file.is_file.return_value = True
        fake_file.suffix = ".jpg"

        self.mock_music_dir.iterdir.return_value = [fake_file]
        tracks = library.discover_tracks()
        self.assertEqual(tracks, [])

    def test_discover_valid_file_defaults(self):
        """
        Expected Result: Returns Track with filename stem and default duration when metadata reading fails or returns None.
        Actual Result: Title='test_song', Duration=180.0
        """
        self.mock_music_dir.exists.return_value = True

        fake_file = MagicMock(spec=Path)
        fake_file.is_file.return_value = True
        fake_file.suffix = ".mp3"
        fake_file.stem = "test_song"

        self.mock_music_dir.iterdir.return_value = [fake_file]

        # Simulate metadata reader returning defaults
        with patch("music_player.library._read_metadata", return_value=("test_song", "Unknown", None)):
            tracks = library.discover_tracks()

        self.assertEqual(len(tracks), 1)
        self.assertEqual(tracks[0].title, "test_song")
        self.assertEqual(tracks[0].duration_seconds, 180.0)

    def test_discover_valid_file_metadata(self):
        """
        Expected Result: Returns Track populated with actual metadata.
        Actual Result: Title='Hit Song', Duration=240.0
        """
        self.mock_music_dir.exists.return_value = True
        fake_file = MagicMock(spec=Path)
        fake_file.is_file.return_value = True
        fake_file.suffix = ".mp3"

        self.mock_music_dir.iterdir.return_value = [fake_file]

        # Simulate successful metadata read
        with patch("music_player.library._read_metadata", return_value=("Hit Song", "Pop Star", 240.0)):
            tracks = library.discover_tracks()

        self.assertEqual(tracks[0].title, "Hit Song")
        self.assertEqual(tracks[0].artist, "Pop Star")
        self.assertEqual(tracks[0].duration_seconds, 240.0)