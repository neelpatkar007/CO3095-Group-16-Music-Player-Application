import unittest
import sys
import importlib
import builtins
from unittest.mock import MagicMock, patch
from pathlib import Path
from music_player import library


class TestLibraryStatement(unittest.TestCase):
    """
    White-Box Statement Test for library.py.
    Testing Tool: Python unittest + unittest.mock + importlib
    Test Technique: Statement Testing (White-Box)
    """
    def test_import_mutagen_missing(self):
        """
        Expected Result: When mutagen cant be imported, ImportError and HAS_MUTAGEN set to False.
        Actual Result: [library] mutagen not available – using filename + defaults only.
        """
        # Save original state
        original_import = builtins.__import__

        def side_effect(name, *args, **kwargs):
            # Only fail if importing mutagen
            if name == 'mutagen':
                raise ImportError("No mutagen")
            return original_import(name, *args, **kwargs)

        # Save original modules
        original_modules = sys.modules.copy()

        try:
            # Remove mutagen from modules so it imports again
            if 'mutagen' in sys.modules:
                del sys.modules['mutagen']

            # Patch __import__ to fail for mutagen
            with patch('builtins.__import__', side_effect=side_effect):
                # Reload library
                importlib.reload(library)

            # Verify fallback state
            self.assertFalse(library.HAS_MUTAGEN)
        finally:
            # Restore original module state
            sys.modules.update(original_modules)
            # Reload again
            importlib.reload(library)

    def test_read_metadata_complex_paths(self):
        """
        Expected Result: All internal exceptions are caught, returning safe default values in their place.
        Actual Result: Passed 100%. The logic survived the exceptions and returned the correct default data.
        """
        path = Path("song.mp3")

        # HAS_MUTAGEN is False
        with patch("music_player.library.HAS_MUTAGEN", False):
            t, a, d = library._read_metadata(path)
            self.assertEqual(t, "song")
            self.assertEqual(d, None)

        # mutagen.File returns None
        with patch("music_player.library.HAS_MUTAGEN", True), \
                patch("music_player.library.mutagen.File", return_value=None):
            t, a, d = library._read_metadata(path)
            self.assertIsNone(d)

        # Tag & Duration Exceptions
        mock_audio = MagicMock()

        # Duration has length, but float conversion fails
        mock_audio.info.length = "invalid_float"

        # Tags exist, but accessing keys fails
        bad_tag = MagicMock()
        bad_tag.__str__.side_effect = Exception("Tag Decode Error")

        mock_audio.tags = {
            "TIT2": bad_tag,  # Title error
            "TPE1": bad_tag  # Artist error
        }

        with patch("music_player.library.HAS_MUTAGEN", True), \
                patch("music_player.library.mutagen.File", return_value=mock_audio):
            t, a, d = library._read_metadata(path)

            self.assertEqual(t, "song")  # Fallback to stem
            self.assertEqual(a, "Unknown")  # Fallback default
            self.assertIsNone(d)  # Fallback None