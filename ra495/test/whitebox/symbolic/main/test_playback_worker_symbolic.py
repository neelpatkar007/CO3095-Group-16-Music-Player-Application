import unittest
from unittest.mock import Mock, patch
import threading
from music_player.main import _playback_worker


class TestSymbolicExecution(unittest.TestCase):

    @patch('music_player.player_core.update_playback')
    @patch('music_player.player_time.check_alarms')
    @patch('time.sleep')
    @patch('time.time')
    def test_pc_1_early_return(self, mock_time, mock_sleep, mock_check_alarms, mock_update_playback):

        state = Mock()
        stop_event = Mock(spec=threading.Event)
        stop_event.is_set.return_value = True

        _playback_worker(state, stop_event)

        mock_update_playback.assert_not_called()
        mock_check_alarms.assert_not_called()

    @patch('music_player.player_core.update_playback')
    @patch('music_player.player_time.check_alarms')
    @patch('time.sleep')
    @patch('time.time')
    def test_pc_2_play_and_alarm(self, mock_time, mock_sleep, mock_check_alarms, mock_update_playback):

        state = Mock()
        state.is_playing = True
        state.is_paused = False
        state.total_play_time = 0.0

        stop_event = Mock(spec=threading.Event)
        stop_event.is_set.side_effect = [False, True]

        mock_time.side_effect = [0.0, 10.0]

        _playback_worker(state, stop_event)

        mock_update_playback.assert_called_once()
        mock_check_alarms.assert_called_once()
        self.assertEqual(state.total_play_time, 10.0)

    @patch('music_player.player_core.update_playback')
    @patch('music_player.player_time.check_alarms')
    @patch('time.sleep')
    @patch('time.time')
    def test_pc_3_play_no_alarm(self, mock_time, mock_sleep, mock_check_alarms, mock_update_playback):

        state = Mock()
        state.is_playing = True
        state.is_paused = False
        state.total_play_time = 0.0

        stop_event = Mock(spec=threading.Event)
        stop_event.is_set.side_effect = [False, True]

        mock_time.side_effect = [0.0, 11.0]

        _playback_worker(state, stop_event)

        mock_update_playback.assert_called_once()
        mock_check_alarms.assert_not_called()

    @patch('music_player.player_core.update_playback')
    @patch('music_player.player_time.check_alarms')
    @patch('time.sleep')
    @patch('time.time')
    def test_pc_4_no_play_alarm(self, mock_time, mock_sleep, mock_check_alarms, mock_update_playback):

        state = Mock()
        state.is_playing = False
        state.is_paused = False
        state.total_play_time = 0.0

        stop_event = Mock(spec=threading.Event)
        stop_event.is_set.side_effect = [False, True]

        mock_time.side_effect = [10.0, 20.0]

        _playback_worker(state, stop_event)

        mock_update_playback.assert_not_called()
        mock_check_alarms.assert_called_once()

    @patch('music_player.player_core.update_playback')
    @patch('music_player.player_time.check_alarms')
    @patch('time.sleep')
    @patch('time.time')
    def test_pc_5_no_play_no_alarm(self, mock_time, mock_sleep, mock_check_alarms, mock_update_playback):

        state = Mock()
        state.is_playing = True
        state.is_paused = True
        state.total_play_time = 0.0

        stop_event = Mock(spec=threading.Event)
        stop_event.is_set.side_effect = [False, True]

        mock_time.side_effect = [0.0, 13.0]

        _playback_worker(state, stop_event)

        mock_update_playback.assert_not_called()
        mock_check_alarms.assert_not_called()


if __name__ == '__main__':
    unittest.main()