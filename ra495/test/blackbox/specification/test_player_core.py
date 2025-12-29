import unittest
from unittest.mock import MagicMock, patch
from music_player import player_core
from music_player.player_state import PlayerState
from music_player.library import Track
from pathlib import Path


class TestPlayerCore(unittest.TestCase):
    """
    Black-Box Specification-based Testing for player_core.py.
    Testing Tool: Python unittest + unittest.mock
    Test Technique: Category Partition Method using TSLGenerator
    Source: playerCore.txt
    """

    def setUp(self):
        # Mock of AudioEngine to simulate the real hardware behaviour
        self.mock_engine = MagicMock()
        self.state = PlayerState([], self.mock_engine)
        self.sample_track = Track(Path("song.mp3"), "Test Song", "Artist", 180)

    # Play Command Tests

    def test_play_error_invalid_state(self):
        """
        Expected Result: The function handles None input without crashing.
        Actual Result: [core] Error: State is None.
        """
        player_core.play(None)

    def test_play_error_no_track(self):
        """
        Expected Result: Playback should not start if current_track is missing.
        Actual Result: [core] No tracks loaded.
        """
        self.state.tracks = []
        self.state.current_index = 0

        player_core.play(self.state)
        self.assertFalse(self.state.is_playing)

    def test_play_already_playing(self):
        """
        Expected Result: Audio engine should not receive any new commands and won't do anything more.
        Actual Result: [core] Already playing.
        """
        self.state.tracks = [self.sample_track]
        self.state.current_index = 0

        self.state.is_playing = True
        self.state.is_paused = False

        player_core.play(self.state)

        self.mock_engine.play.assert_not_called()

    def test_play_resume(self):
        """
        Expected Result: Audio engine resumes.
        Actual Result: [core] Resumed: Test Song – Artist
        """
        self.state.tracks = [self.sample_track]
        self.state.current_index = 0

        self.state.is_playing = True
        self.state.is_paused = True

        player_core.play(self.state)

        self.assertFalse(self.state.is_paused)
        self.mock_engine.resume.assert_called_once()

    def test_play_start_fresh(self):
        """
        Expected Result: Audio engine starts playing file from 0.0s.
        Actual Result: [core] Playing: Test Song – Artist (1.5x)
        """
        self.state.tracks = [self.sample_track]
        self.state.current_index = 0

        self.state.is_playing = False
        self.state.is_paused = False
        self.state.playback_speed = 1.5

        player_core.play(self.state)

        self.assertTrue(self.state.is_playing)
        self.mock_engine.play.assert_called_with(self.sample_track.path, start_pos=0.0, speed=1.5)

    # Pause Command Tests

    def test_pause_successful(self):
        """
        Expected Result: State updates to paused and engine pauses.
        Actual Result: [core] Paused.
        """
        self.state.is_playing = True
        self.state.is_paused = False

        player_core.pause(self.state)

        self.assertTrue(self.state.is_paused)
        self.mock_engine.pause.assert_called_once()

    def test_pause_noop(self):
        """
        Expected Result: No action taken if not currently playing.
        Actual Result: [core] Nothing to pause.
        """
        self.state.is_playing = False
        player_core.pause(self.state)
        self.mock_engine.pause.assert_not_called()