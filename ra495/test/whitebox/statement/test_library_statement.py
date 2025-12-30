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

