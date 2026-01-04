import unittest
from unittest.mock import MagicMock, patch
from music_player.player_core import set_playback_speed, play
from music_player.player_state import PlayerState


class TestConcolicExecution(unittest.TestCase):


    def create_state(self, speed=1.0, playing=False, paused=False):
        """Helper to create a PlayerState with a mocked audio engine."""
        state = PlayerState(tracks=[], audio_engine=MagicMock())
        state.playback_speed = speed
        state.is_playing = playing
        state.is_paused = paused
        return state

    def test_iteration_1_flip_state_type(self):
        """Iteration 1: Early exit when state is invalid type."""
        s1 = "NotAStateObject"
        s2 = 1.0
        result = set_playback_speed(s1, s2)
        self.assertIsNone(result)

    def test_iteration_2_flip_speed_type(self):
        """Iteration 2: Speed type invalid (not a number)."""
        s1 = self.create_state()
        s2 = "NotANumber"

        with patch('builtins.print') as mock_print:
            set_playback_speed(s1, s2)
            mock_print.assert_called_with("[core] Error: Speed must be a number.")

    def test_iteration_3_flip_range_lower(self):
        """Iteration 3: Speed below allowed range."""
        s1 = self.create_state()
        s2 = 0.1  # Below 0.5

        with patch('builtins.print') as mock_print:
            set_playback_speed(s1, s2)
            mock_print.assert_called_with("[core] Speed must be between 0.5x and 2.0x.")

    def test_iteration_4_flip_redundancy(self):
        """Iteration 4: Speed same as current triggers redundancy message."""
        s1 = self.create_state(speed=1.0)
        s2 = 1.0

        with patch('builtins.print') as mock_print:
            set_playback_speed(s1, s2)
            mock_print.assert_called_with(f"[core] Speed is already {s2}x.")

    @patch('music_player.player_core.play')
    def test_iteration_5_flip_is_playing(self, mock_play):
        """Iteration 5: Speed change while playing calls play() internally."""
        s1 = self.create_state(speed=1.0, playing=True)
        s2 = 1.5

        with patch('builtins.print') as mock_print:
            set_playback_speed(s1, s2)
            # The play() function will be called to apply new speed
            mock_play.assert_called_once()

    def test_iteration_6_flip_is_paused(self):
        """Iteration 6: Speed change while paused displays message."""
        s1 = self.create_state(speed=1.0, playing=False, paused=True)
        s2 = 1.5

        with patch('builtins.print') as mock_print:
            set_playback_speed(s1, s2)
            mock_print.assert_called_with("[core] New speed will apply when you resume playback.")

    def test_iteration_7_clean_run(self):
        """Iteration 7: Speed change while stopped applies normally."""
        s1 = self.create_state(speed=1.0, playing=False, paused=False)
        s2 = 1.5

        with patch('builtins.print') as mock_print:
            set_playback_speed(s1, s2)
            self.assertEqual(s1.playback_speed, 1.5)
            mock_print.assert_called_with(f"[core] Playback speed set to {s2}x.")


if __name__ == '__main__':
    unittest.main()
