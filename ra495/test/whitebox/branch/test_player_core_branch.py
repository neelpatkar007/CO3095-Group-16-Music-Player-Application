import unittest
from unittest.mock import MagicMock, patch
from music_player import player_core
from music_player.player_state import PlayerState
from music_player.library import Track
from pathlib import Path


class TestPlayerCoreBranch(unittest.TestCase):
    """
    White-Box Branch Testing for player_core.py.
    Testing Tool: Python unittest + unittest.mock
    Test Technique: White-Box Branch Testing
    """

    def setUp(self):
        self.mock_engine = MagicMock()
        self.state = PlayerState([], self.mock_engine)
        self.sample_track = Track(Path("song.mp3"), "Test Song", "Artist", 180)

    def test_play_branches(self):
        """
        Branches:
         - Track None
         - Already Playing
         - Is Paused
        Expected Result:
         - No tracks loaded message.
         - Already playing message.
         - Resumes or starts fresh playback.
        Actual Result:
            [core] No tracks loaded.

            [core] Already playing.

            [core] Resumed: Test Song – Artist
            [core] Playing: Test Song – Artist (1.0x)
        """
        # Track is None (True)
        self.state.tracks = []
        self.state.current_index = 0
        player_core.play(self.state)

        # Already Playing (True)
        self.state.tracks = [self.sample_track]
        self.state.is_playing = True
        player_core.play(self.state)

        # Resume vs Fresh (True/False)
        self.state.is_paused = True
        player_core.play(self.state)

        self.state.is_paused = False
        self.state.is_playing = False
        player_core.play(self.state)

    def test_update_branches(self):
        """
        Branches:
         - Sleep Timer Triggered
         - Track Finished
        Expected Result:
         - Stops playback when timer expires.
        Actual Result:
            [timer] Sleep timer reached. Stopping playback.
            [core] Stopped.
        """
        self.state.is_playing = True
        self.state.tracks = [self.sample_track]

        # Sleep Timer (True)
        self.state.sleep_deadline = 100
        with patch('time.time', return_value=200):
            player_core.update_playback(self.state, 1.0)
        self.assertFalse(self.state.is_playing)

        # Track Finished (True/False)
        self.state.is_playing = True
        self.state.position_seconds = 10.0  # False
        player_core.update_playback(self.state, 1.0)

        self.state.position_seconds = 180.0  # True
        with patch('music_player.player_queue.next_track') as mock_next:
            player_core.update_playback(self.state, 1.0)
            mock_next.assert_called()

    def test_timer_branches(self):
        """
        Branches:
         - Cancel Input
         - Timer Exists
        Expected Result:
         - Cancels timer (sleep_deadline = None).
         - Sets new timer.
        Actual Result:
            [core] Warning: Timer set but nothing is currently playing.

            [core] Sleep timer set for 10 minutes.
            [core] Replacing 10.0m timer.
            [core] Warning: Timer set but nothing is currently playing.
            [core] Sleep timer set for 20 minutes.
        """
        # Cancel (True)
        player_core.set_sleep_timer(self.state, 0)

        # Overwrite Logic (True/False)
        # False path (New timer)
        self.state.sleep_deadline = None
        player_core.set_sleep_timer(self.state, 10)

        # True path (Overwrite existing)
        with patch('time.time', return_value=1000):
            self.state.sleep_deadline = 1600
            player_core.set_sleep_timer(self.state, 20)