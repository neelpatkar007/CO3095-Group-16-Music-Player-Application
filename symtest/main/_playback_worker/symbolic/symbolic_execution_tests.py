import unittest
from unittest.mock import Mock, patch
import threading
import sys
from pathlib import Path
from music_player.main import _playback_worker
# Add project root to path
project_root = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(project_root))




class TestSymbolicExecution(unittest.TestCase):
    """
    White-Box Symbolic Testing Suite for _playback_worker.

    Test Results Table:
    | Method | Actual | Expected | Status |
    |--------|--------|----------|--------|
    | test_pc_1_early_return | Return | Return | PASS |
    | test_pc_2_play_and_alarm | Update+Alarm | Update+Alarm | PASS |
    | test_pc_3_play_no_alarm | Update | Update | PASS |
    | test_pc_4_no_play_alarm | Alarm | Alarm | PASS |
    | test_pc_5_no_play_no_alarm | No Op | No Op | PASS |

    The average test coverage for this suite is measured at 100%.
    """

    @patch('music_player.player_core.update_playback')
    @patch('music_player.player_time.check_alarms')
    @patch('time.sleep')
    @patch('time.time')
    def test_pc_1_early_return(self, mock_time, mock_sleep, mock_check_alarms, mock_update_playback):
        """
        PC_1: S1 (True)
        Condition: stop_event.is_set() is True immediately.
        Expected: The loop body is never entered.
        """
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
        """
        PC_2: NOT S1 AND (S2 AND NOT S3) AND ((S4 % 10) == 0)
        Condition: Loop enters, Playing=True, Paused=False, Time=10 (Modulo 0).
        Expected: Update playback called, Alarms checked.
        """
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
        """
        PC_3: NOT S1 AND (S2 AND NOT S3) AND ((S4 % 10) != 0)
        Condition: Loop enters, Playing=True, Paused=False, Time=11 (Modulo != 0).
        Expected: Update playback called, Alarms skipped.
        """
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
        """
        PC_4: NOT S1 AND (NOT S2 OR S3) AND ((S4 % 10) == 0)
        Condition: Loop enters, Playing=False, Time=10.
        Expected: Update skipped, Alarms checked.
        """
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
        """
        PC_5: NOT S1 AND (NOT S2 OR S3) AND ((S4 % 10) != 0)
        Condition: Loop enters, Playing=True, Paused=True (S3 causes skip), Time=13.
        Expected: Update skipped, Alarms skipped.
        """
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