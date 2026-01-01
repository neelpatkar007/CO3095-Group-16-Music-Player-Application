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

class TestPlayerQueueCoverage(unittest.TestCase):
    """
    Whitebox Branch Testing for player_queue.py.
    Tool: Python unittest + unittest.mock
    Technique: White-Box Branch Testing
    """

    def setUp(self):
        """
        Setup valid PlayerState with 3 tracks for each test.
        """
        self.track1 = Track(Path("song1.mp3"), "Song 1", "Artist 1", 180)
        self.track2 = Track(Path("song2.mp3"), "Song 2", "Artist 2", 200)
        self.track3 = Track(Path("song3.mp3"), "Song 3", "Artist 3", 210)

        self.state = MagicMock()
        self.state.tracks = [self.track1, self.track2, self.track3]
        self.state.library_tracks = [self.track1, self.track2, self.track3]
        self.state.current_index = 0
        self.state.current_track = self.track1
        self.state.history = []
        self.state.audio_engine = MockAudioEngine()
        self.state.is_playing = False
        self.state.is_paused = False
        self.state.loop_mode = "off"
        self.state.shuffle_active = False
        self.state.position_seconds = 0.0
        self.state.playlists = []