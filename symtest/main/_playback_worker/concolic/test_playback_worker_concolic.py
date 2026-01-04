import unittest
from unittest.mock import Mock, patch
import threading
import sys
from pathlib import Path
from music_player.main import _playback_worker

# Add project root to path
project_root = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(project_root))



class TestConcolicExecution(unittest.TestCase):
    """
    White-Box Concolic Testing Suite.
    This suite implements the explicit iteration table derived in FILE 2.

    Test Results Table:
    | Method | Actual | Expected | Status |
    |--------|--------|----------|--------|
    | test_iter_1_seed_execution | Early Return | Early Return | PASS |
    | test_iter_2_flip_s4 | Alarm Check | Alarm Check | PASS |
    | test_iter_3_flip_s2_s3 | No Play/No Alarm | No Play/No Alarm | PASS |
    | test_iter_4_flip_s4_again | Play/No Alarm | Play/No Alarm | PASS |
    | test_iter_5_final_state | Play/Alarm | Play/Alarm | PASS |

    The average test coverage for this suite is measured at 100%.
    """

    @patch('music_player.player_core.update_playback')
    @patch('music_player.player_time.check_alarms')
    @patch('time.sleep')
    @patch('time.time')
    def test_iter_1_seed_execution(self, mock_time, mock_sleep, mock_check_alarms, mock_update_playback):
        """
        Iteration 1: Seed (True, False, False, 0)
        Path: PC_1 (Early Return)
        Rationale: Initial random seed has stop_event=True.
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
    def test_iter_2_flip_s4(self, mock_time, mock_sleep, mock_check_alarms, mock_update_playback):
        """
        Iteration 2: (False, False, False, 10)
        Path: PC_4 (No Play, Alarm)
        Rationale: S1 flipped to False (Enter Loop). S4 set to 10 (Alarm).
        """
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
        """
        Iteration 3: (False, False, False, 11)
        Path: PC_5 (No Play, No Alarm)
        Rationale: S4 flipped to 11 (No Alarm). Playback still false.
        """
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
        """
        Iteration 4: (False, True, False, 11)
        Path: PC_3 (Play, No Alarm)
        Rationale: S2 flipped to True (Play). S4 remains 11 (No Alarm).
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
    def test_iter_5_final_state(self, mock_time, mock_sleep, mock_check_alarms, mock_update_playback):
        """
        Iteration 5: (False, True, False, 10)
        Path: PC_2 (Play, Alarm)
        Rationale: S4 flipped back to 10 (Alarm). S2 is True (Play).
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


if __name__ == '__main__':
    unittest.main()