import unittest
from unittest.mock import MagicMock, patch
from music_player.player_core import set_playback_speed, play
from music_player.player_state import PlayerState


class TestSymbolicExecution(unittest.TestCase):


    def setUp(self):
        self.state = PlayerState(tracks=[], audio_engine=MagicMock())
        self.state.playback_speed = 1.0
        self.state.is_playing = False
        self.state.is_paused = False

    def test_pc_1_invalid_state_type(self):
        result = set_playback_speed("InvalidState", 1.0)
        self.assertIsNone(result)

    def test_pc_3_invalid_speed_type(self):
        with patch('builtins.print') as mock_print:
            set_playback_speed(self.state, "Fast")
            mock_print.assert_called_with("[core] Error: Speed must be a number.")

    def test_pc_4_speed_out_of_range(self):
        with patch('builtins.print') as mock_print:
            set_playback_speed(self.state, 0.4)
            mock_print.assert_called_with("[core] Speed must be between 0.5x and 2.0x.")

        with patch('builtins.print') as mock_print:
            set_playback_speed(self.state, 2.1)
            mock_print.assert_called_with("[core] Speed must be between 0.5x and 2.0x.")

    def test_pc_5_redundant_speed(self):
        self.state.playback_speed = 1.0
        s2 = 1.0
        with patch('builtins.print') as mock_print:
            set_playback_speed(self.state, s2)
            mock_print.assert_called_with(f"[core] Speed is already {s2}x.")

    @patch('music_player.player_core.play')
    def test_pc_6_is_playing_restart(self, mock_play):
        self.state.is_playing = True
        s2 = 1.5
        with patch('builtins.print') as mock_print:
            set_playback_speed(self.state, s2)
            self.assertFalse(self.state.is_playing)
            self.assertEqual(self.state.playback_speed, s2)
            mock_play.assert_called_once_with(self.state)

    def test_pc_7_is_paused_message(self):
        self.state.is_paused = True
        s2 = 1.5
        with patch('builtins.print') as mock_print:
            set_playback_speed(self.state, s2)
            self.assertEqual(self.state.playback_speed, s2)
            mock_print.assert_called_with("[core] New speed will apply when you resume playback.")

    def test_pc_8_silent_update(self):
        self.state.is_playing = False
        self.state.is_paused = False
        s2 = 1.5
        with patch('builtins.print') as mock_print:
            set_playback_speed(self.state, s2)
            self.assertEqual(self.state.playback_speed, s2)
            mock_print.assert_called_with(f"[core] Playback speed set to {s2}x.")


if __name__ == '__main__':
    unittest.main()
