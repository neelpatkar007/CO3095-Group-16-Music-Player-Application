import unittest
from unittest.mock import MagicMock, patch
from music_player.player_core import update_playback
from music_player.player_state import PlayerState


class Track:
    pass


class TestSymbolicExecution(unittest.TestCase):

    def setUp(self):
        self.state = MagicMock(spec=PlayerState)
        self.state.playback_speed = 1.0
        self.state.position_seconds = 10.0
        self.state.is_playing = True
        self.state.is_paused = False
        self.state.sleep_deadline = None
        self.state.current_track = MagicMock()
        self.state.current_track.duration_seconds = 100.0

    def test_pc_1(self):
        invalid_state = "Not A State Object"
        delta = 1.0

        update_playback(invalid_state, delta)
        self.assertTrue(True)

    def test_pc_2(self):
        delta = "Not A Number"

        update_playback(self.state, delta)
        self.assertEqual(self.state.position_seconds, 10.0)

    @patch('music_player.player_core.stop')
    @patch('music_player.player_core.time.time')
    def test_pc_3(self, mock_time_func, mock_stop):
        self.state.sleep_deadline = 1000.0
        mock_time_func.return_value = 1001.0

        update_playback(self.state, 1.0)

        mock_stop.assert_called_once_with(self.state)
        self.assertIsNone(self.state.sleep_deadline)

    @patch('music_player.player_core.time.time')
    def test_pc_4(self, mock_time_func):
        mock_time_func.return_value = 500.0
        self.state.sleep_deadline = 1000.0
        delta = -5.0
        update_playback(self.state, delta)
        self.assertEqual(self.state.position_seconds, 10.0)

    def test_pc_5(self):
        self.state.is_playing = False
        update_playback(self.state, 1.0)
        self.assertEqual(self.state.position_seconds, 10.0)
        self.state.is_playing = True
        self.state.is_paused = True
        update_playback(self.state, 1.0)
        self.assertEqual(self.state.position_seconds, 10.0)

    def test_pc_6(self):
        self.state.current_track = None
        update_playback(self.state, 1.0)
        self.assertEqual(self.state.position_seconds, 11.0)

    @patch('music_player.player_core.player_metrics')
    @patch('music_player.player_core.player_queue')
    def test_pc_7(self, mock_queue, mock_metrics):
        self.state.position_seconds = 99.0
        self.state.current_track.duration_seconds = 100.0
        delta = 2.0
        update_playback(self.state, delta)
        mock_metrics.record_play.assert_called_once_with(self.state)
        self.assertEqual(self.state.position_seconds, 100.0)
        mock_queue.next_track.assert_called_once_with(self.state)

    @patch('music_player.player_core.player_metrics')
    def test_pc_8(self, mock_metrics):
        self.state.position_seconds = 10.0
        self.state.current_track.duration_seconds = 100.0
        delta = 1.0
        update_playback(self.state, delta)
        self.assertEqual(self.state.position_seconds, 11.0)
        mock_metrics.record_play.assert_not_called()


if __name__ == '__main__':
    unittest.main()