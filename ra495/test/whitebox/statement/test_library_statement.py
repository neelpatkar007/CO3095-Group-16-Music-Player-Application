import unittest
import sys
import importlib
import builtins
from unittest.mock import MagicMock, patch
from pathlib import Path
from music_player import library


class TestLibraryStatement(unittest.TestCase):

    def test_import_mutagen_missing(self):

        original_import = builtins.__import__

        def side_effect(name, *args, **kwargs):
            if name == 'mutagen':
                raise ImportError("No mutagen")
            return original_import(name, *args, **kwargs)

        original_modules = sys.modules.copy()

        try:
            if 'mutagen' in sys.modules:
                del sys.modules['mutagen']

            with patch('builtins.__import__', side_effect=side_effect):
                importlib.reload(library)

            self.assertFalse(library.HAS_MUTAGEN)
        finally:
            sys.modules.update(original_modules)
            importlib.reload(library)

    def test_read_metadata_complex_paths(self):
        path = Path("song.mp3")

        with patch("music_player.library.HAS_MUTAGEN", False):
            t, a, d = library._read_metadata(path)
            self.assertEqual(t, "song")
            self.assertEqual(d, None)

        with patch("music_player.library.HAS_MUTAGEN", True), \
                patch("music_player.library.mutagen.File", return_value=None):
            t, a, d = library._read_metadata(path)
            self.assertIsNone(d)

        mock_audio = MagicMock()

        mock_audio.info.length = "invalid_float"

        bad_tag = MagicMock()
        bad_tag.__str__.side_effect = Exception("Tag Decode Error")

        mock_audio.tags = {
            "TIT2": bad_tag,
            "TPE1": bad_tag
        }

        with patch("music_player.library.HAS_MUTAGEN", True), \
                patch("music_player.library.mutagen.File", return_value=mock_audio):
            t, a, d = library._read_metadata(path)

            self.assertEqual(t, "song")
            self.assertEqual(a, "Unknown")
            self.assertIsNone(d)

    def test_read_metadata_title_artist_duration(self):
        with patch("music_player.library.MUSIC_DIR") as mock_dir:
            mock_dir.exists.return_value = True

            p_file = MagicMock()
            p_file.is_file.return_value = True
            p_file.suffix = ".mp3"

            mock_dir.iterdir.return_value = [p_file]

            with patch("music_player.library._read_metadata", return_value=("Title", "Artist", 100)):
                library.discover_tracks()