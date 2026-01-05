import unittest
from unittest.mock import MagicMock, patch, mock_open
from music_player.player_config import save_settings

class TestConcolicExecution(unittest.TestCase):

    def setUp(self):
        self.concrete_state = MagicMock()
        self.concrete_state.volume = 50
        self.concrete_state.shuffle_active = False
        self.concrete_state.loop_mode = "one"
        self.concrete_state.playback_speed = 1.5
        self.concrete_state.song_tags = {}
        self.concrete_state.total_play_time = 0.0

    def test_iteration_1_initial_seed(self):
        S1 = None

        with patch("builtins.open", mock_open()) as mock_file:
            save_settings(S1)
            mock_file.assert_not_called()

    @patch("builtins.print")
    def test_iteration_2_flip_s1_constraint(self, mock_print):
        S1 = self.concrete_state

        with patch("builtins.open", mock_open()) as mock_file:
            save_settings(S1)
            mock_file.assert_called()
            mock_print.assert_called_with("[config] Settings saved.")

    @patch("builtins.print")
    def test_iteration_3_flip_s2_constraint(self, mock_print):
        S1 = self.concrete_state

        with patch("builtins.open", mock_open()) as mock_file:
            mock_file.side_effect = OSError("Disk Full")
            save_settings(S1)
            mock_print.assert_called_with("[config] Error saving settings: Disk Full")


if __name__ == '__main__':
    unittest.main()