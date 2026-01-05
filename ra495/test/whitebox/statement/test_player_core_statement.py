import unittest
from unittest.mock import MagicMock, patch
from music_player import player_core
from music_player.player_state import PlayerState
from music_player.library import Track
from pathlib import Path


class TestPlayerCoreStatement(unittest.TestCase):


    def setUp(self):
        self.mock_engine = MagicMock()
        self.state = PlayerState([], self.mock_engine)
        self.sample_track = Track(Path("song.mp3"), "Test Song", "Artist", 180)


    def test_play_errors(self):

        player_core.play(None)

        self.state.tracks = []
        player_core.play(self.state)

    def test_play_execution_paths(self):

        self.state.tracks = [self.sample_track]
        self.state.current_index = 0

        self.state.is_paused = True
        player_core.play(self.state)
        self.mock_engine.resume.assert_called()

        self.state.is_paused = False
        self.state.is_playing = False
        player_core.play(self.state)
        self.mock_engine.play.assert_called()


    def test_pause_stop_logic(self):

        self.state.is_playing = True
        player_core.pause(self.state)
        self.assertTrue(self.state.is_paused)


        player_core.stop(self.state)
        self.assertEqual(self.state.position_seconds, 0.0)


    def test_update_playback_flow(self):
        self.state.is_playing = True
        self.state.tracks = [self.sample_track]

        player_core.update_playback(self.state, 5.0)
        self.assertEqual(self.state.position_seconds, 5.0)

        self.state.position_seconds = 180.0
        with patch('music_player.player_queue.next_track') as mock_next:
            player_core.update_playback(self.state, 1.0)
            mock_next.assert_called()


    def test_sleep_timer_logic(self):

        with patch('time.time', return_value=1000):
            player_core.set_sleep_timer(self.state, 10)
        self.assertEqual(self.state.sleep_deadline, 1600)

        player_core.set_sleep_timer(self.state, 0)
        self.assertIsNone(self.state.sleep_deadline)


    def test_set_speed(self):
        player_core.set_playback_speed(self.state, 1.5)
        self.assertEqual(self.state.playback_speed, 1.5)