import unittest
from unittest.mock import MagicMock, patch, PropertyMock
from music_player import player_queue
from music_player.library import Track
from pathlib import Path


class MockAudioEngine:
    """
    Simulates the AudioBackend for testing playback logic without real audio.
    """

    def __init__(self):
        self.stop_called = False
        self.play_called = False

    def stop(self):
        self.stop_called = True

    def play(self, path, start_pos=0.0):
        self.play_called = True

    def is_busy(self):
        return False