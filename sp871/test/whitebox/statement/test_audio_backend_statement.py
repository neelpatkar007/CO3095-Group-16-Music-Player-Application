import unittest
import sys
import importlib
import builtins
from unittest.mock import MagicMock, patch
from pathlib import Path
from music_player import audio_backend


class TestAudioBackendStatement(unittest.TestCase):


    def test_import_failures(self):

        original_import = builtins.__import__

        def side_effect(name, *args, **kwargs):
            if name == 'pygame':
                raise ImportError("No pygame")
            if name == 'pydub':
                raise ImportError("No pydub")
            return original_import(name, *args, **kwargs)

        original_modules = sys.modules.copy()

        try:
            # Remove modules to force reload
            if 'pygame' in sys.modules: del sys.modules['pygame']
            if 'pydub' in sys.modules: del sys.modules['pydub']

            # Patch import to fail
            with patch('builtins.__import__', side_effect=side_effect):
                importlib.reload(audio_backend)

            # Verify flags are False
            self.assertFalse(audio_backend.HAS_PYGAME)
            self.assertFalse(audio_backend.HAS_PYDUB)

        finally:
            sys.modules.update(original_modules)
            importlib.reload(audio_backend)

    def test_exception_handlers(self):

        engine = audio_backend.AudioEngine()
        path = Path("test.mp3")

        # Speed Processing Exception
        # Pydub enabled and AudioSegment raises error
        with patch("music_player.audio_backend.HAS_PYDUB", True), \
                patch("music_player.audio_backend.AudioSegment.from_file", side_effect=Exception("Pydub Fail")), \
                patch("music_player.audio_backend.HAS_PYGAME", False):  # Simulated playback

            engine.play(path, speed=1.5)
            # Verify fallback occurred
            self.assertEqual(engine.current_speed, 1.0)

        # Real Playback Exception
        # Pygame enabled but load() raises error
        with patch("music_player.audio_backend.HAS_PYGAME", True), \
                patch("music_player.audio_backend.pygame") as mock_pg:
            mock_pg.mixer.music.load.side_effect = Exception("Pygame Load Fail")
            engine.play(path)  # prints error

        # Real Seek Exception
        with patch("music_player.audio_backend.HAS_PYGAME", True), \
                patch("music_player.audio_backend.pygame") as mock_pg:
            engine.current_path = path
            mock_pg.mixer.music.load.side_effect = Exception("Seek Fail")
            engine.seek(10.0)  # prints error