import unittest
import sys
import importlib
import builtins
from unittest.mock import MagicMock, patch
from pathlib import Path
from music_player import audio_backend


class TestAudioBackendStatement(unittest.TestCase):
    """
    White-Box Statement Tests for audio_backend.py.
    Testing Tool: Python unittest + unittest.mock + importlib
    Test Technique: White-Box Statement Testing
    """

    def test_import_failures(self):
        """
        Expected Result:
         - HAS_PYGAME and HAS_PYDUB flags are set to False when imports fail.
         - Warning messages are printed.
        Actual Result:
            PASSED [100%][audio] pygame not available – using simulated audio backend.
            [audio] pydub not found. Speed changes will be simulated.
        """
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
        """
        Expected Result:
         - Speed Error: Fallback to 1.0x speed.
         - Playback/Seek Error: Error is caught and printed, application does not crash.
        Actual Result:
            PASSED [100%][audio] Processing audio for 1.5x speed... (this may take a moment)
            [audio] Error processing speed: Pydub Fail. Falling back to 1.0x.
            [audio] PLAY (simulated) test.mp3 from 0.0s
            [audio] ERROR playing test.mp3: Pygame Load Fail
            [audio] ERROR seeking: Seek Fail
        """
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