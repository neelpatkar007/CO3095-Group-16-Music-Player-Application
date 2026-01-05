import unittest
from unittest.mock import MagicMock, patch
from music_player.main import handle_command

class TestConcolicExecution(unittest.TestCase):

    def setUp(self):
        self.mock_state = MagicMock()
        self.mock_state.resume_active = False
        self.mock_state.current_track = None
        self.mock_state.position_seconds = 0.0

    def run_concolic_step(self, s1_command, s2_resume, s3_track, s4_pos):
        """Helper to inject concrete values derived from symbolic solving."""
        self.mock_state.resume_active = s2_resume
        self.mock_state.current_track = s3_track
        self.mock_state.position_seconds = s4_pos
        return handle_command(self.mock_state, s1_command)

    @patch('music_player.player_core.play')
    @patch('music_player.player_seek.seek_to')
    @patch('music_player.player_shortcuts.handle_keypress')
    def test_iterative_path_discovery(self, mock_keypress, mock_seek, mock_play):

        self.run_concolic_step("", False, None, 0.0)
        self.run_concolic_step("p", False, None, 0.0)
        mock_keypress.assert_called()
        with patch('music_player.player_metrics.save_data') as mock_save:
            res = self.run_concolic_step("/quit", False, None, 0.0)
            self.assertFalse(res)

        self.run_concolic_step("/play", False, None, 0.0)
        mock_play.assert_called()
        self.run_concolic_step("/play", True, MagicMock(), 0.0)
        mock_seek.reset_mock()
        self.run_concolic_step("/play", True, MagicMock(), 155.0)
        mock_seek.assert_called_with(self.mock_state, "155.0")

    @patch('music_player.player_seek.seek_to')
    def test_argument_boundary_conditions(self, mock_seek):

        with patch('builtins.print') as mock_print:
            self.run_concolic_step("/seek", False, None, 0.0)
            mock_print.assert_called_with("[main] Usage: /seek <mm:ss or seconds>")

        self.run_concolic_step("/seek 120", False, None, 0.0)
        mock_seek.assert_called()


if __name__ == '__main__':
    unittest.main()