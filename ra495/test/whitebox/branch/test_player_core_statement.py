import unittest
from unittest.mock import MagicMock, patch
from music_player import player_core
from music_player.player_state import PlayerState
from music_player.library import Track
from pathlib import Path


class TestPlayerCoreStatement(unittest.TestCase):
    """
    White-Box Statement Testing for player_core.py.
    Testing Tool: Python unittest + unittest.mock
    Test Technique: White-Box Statement Testing
    """

    def setUp(self):
        self.mock_engine = MagicMock()
        self.state = PlayerState([], self.mock_engine)
        self.sample_track = Track(Path("song.mp3"), "Test Song", "Artist", 180)

    # Play Tests

    def test_play_errors(self):
        """
        Expected Result: Handles None state and missing tracks without crashing.
        Actual Result:
            [core] Error: State is None.
            [core] No tracks loaded.
        """
        # Test None state
        player_core.play(None)

        # Test No Tracks
        self.state.tracks = []
        player_core.play(self.state)

    def test_play_execution_paths(self):
        """
        Expected Result: Covers Resume and Fresh Start logic.
        Actual Result:
            [core] Resumed: Test Song – Artist
            [core] Playing: Test Song – Artist (1.0x)
        """
        self.state.tracks = [self.sample_track]
        self.state.current_index = 0

        # Resume
        self.state.is_paused = True
        player_core.play(self.state)
        self.mock_engine.resume.assert_called()

        # Fresh Play
        self.state.is_paused = False
        self.state.is_playing = False
        player_core.play(self.state)
        self.mock_engine.play.assert_called()

    # Pause and Stop Tests

    def test_pause_stop_logic(self):
        """
        Expected Result: Pause and Stop update flags correctly.
        Actual Result:
            [core] Paused.
            [core] Stopped.
        """
        # Pause
        self.state.is_playing = True
        player_core.pause(self.state)
        self.assertTrue(self.state.is_paused)

        # Stop
        player_core.stop(self.state)
        self.assertEqual(self.state.position_seconds, 0.0)

    # Update Playback Tests

    def test_update_playback_flow(self):
        """
        Expected Result: Update position and handle track finish.
        Actual Result: Position increments and next_track is called on finish.
        """
        self.state.is_playing = True
        self.state.tracks = [self.sample_track]

        # Normal Update
        player_core.update_playback(self.state, 5.0)
        self.assertEqual(self.state.position_seconds, 5.0)

        # Track Finished
        self.state.position_seconds = 180.0
        with patch('music_player.player_queue.next_track') as mock_next:
            player_core.update_playback(self.state, 1.0)
            mock_next.assert_called()

    # Sleep Timer Tests

    def test_sleep_timer_logic(self):
        """
        Expected Result: Sets valid timer and handles cancellation.
        Actual Result:
            [core] Warning: Timer set but nothing is currently playing.
            [core] Sleep timer set for 10 minutes.
            [core] Sleep timer cancelled.
        """
        # Valid Set
        with patch('time.time', return_value=1000):
            player_core.set_sleep_timer(self.state, 10)
        self.assertEqual(self.state.sleep_deadline, 1600)

        # Cancel
        player_core.set_sleep_timer(self.state, 0)
        self.assertIsNone(self.state.sleep_deadline)