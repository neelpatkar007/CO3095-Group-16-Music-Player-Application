import unittest
from unittest.mock import Mock, patch
import threading
from music_player.main import _playback_worker

class TestConcolicExecution(unittest.TestCase):

    @patch('music_player.player_core.update_playback')
    @patch('music_player.player_time.check_alarms')
    @patch('time.sleep')
    @patch('time.time')
    def test_iter_1_seed_execution(self, mock_time, mock_sleep, mock_check_alarms, mock_update_playback):

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
    def test_iter_2_flip_s4(self, mock_time, mock_sleep, mock_check_alarms, mock_update_playback):

        state = Mock()
        state.is_playing = False
        state.is_paused = False
        state.total_play_time = 0.0
        stop_event = Mock(spec=threading.Event)
        stop_event.is_set.side_effect = [False, True]
        mock_time.side_effect = [0.0, 10.0]

        _playback_worker(state, stop_event)

        mock_update_playback.assert_not_called()
        mock_check_alarms.assert_called_once()

    @patch('music_player.player_core.update_playback')
    @patch('music_player.player_time.check_alarms')
    @patch('time.sleep')
    @patch('time.time')
    def test_iter_3_flip_s2_s3(self, mock_time, mock_sleep, mock_check_alarms, mock_update_playback):

        state = Mock()
        state.is_playing = False
        state.is_paused = False
        state.total_play_time = 0.0
        stop_event = Mock(spec=threading.Event)
        stop_event.is_set.side_effect = [False, True]
        mock_time.side_effect = [0.0, 11.0]

        _playback_worker(state, stop_event)

        mock_update_playback.assert_not_called()
        mock_check_alarms.assert_not_called()

    @patch('music_player.player_core.update_playback')
    @patch('music_player.player_time.check_alarms')
    @patch('time.sleep')
    @patch('time.time')
    def test_iter_4_flip_s4_again(self, mock_time, mock_sleep, mock_check_alarms, mock_update_playback):

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
    def test_iter_5_final_state(self, mock_time, mock_sleep, mock_check_alarms, mock_update_playback):

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


if __name__ == '__main__':
    unittest.main()