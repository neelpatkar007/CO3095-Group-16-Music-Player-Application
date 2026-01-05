import unittest
from unittest.mock import patch, MagicMock, mock_open
from music_player.player_config import save_settings

class SymbolicSaveSettingsTests(unittest.TestCase):
    def setUp(self):
        self.symbolic_state = MagicMock()
        self.symbolic_state.volume = 50
        self.symbolic_state.shuffle_active = False
        self.symbolic_state.loop_mode = "one"
        self.symbolic_state.playback_speed = 1.5
        self.symbolic_state.song_tags = {}
        self.symbolic_state.total_play_time = 0.0

    def test_path_pc1_null_state(self):
        S1 = None
        with patch("builtins.open", mock_open()) as mock_file:
            save_settings(S1)
            mock_file.assert_not_called()

    def test_path_pc2_successful_write(self):
        S1 = self.symbolic_state
        with patch("builtins.open", mock_open()) as mock_file, patch("builtins.print") as mock_print:
            save_settings(S1)
            mock_file.assert_called()
            mock_print.assert_called_with("[config] Settings saved.")

    def test_path_pc3_filesystem_error(self):
        S1 = self.symbolic_state
        with patch("builtins.open", mock_open()) as mock_file, patch("builtins.print") as mock_print:
            mock_file.side_effect = OSError("Disk Full")
            save_settings(S1)
            mock_print.assert_called_with("[config] Error saving settings: Disk Full")

if __name__ == "__main__":
    unittest.main()
