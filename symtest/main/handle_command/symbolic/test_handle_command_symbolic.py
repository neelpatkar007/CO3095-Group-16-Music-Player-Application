import unittest
from unittest.mock import MagicMock, patch
from music_player.main import handle_command

class TestSymbolicExecution(unittest.TestCase):

    def setUp(self):
        self.mock_state = MagicMock()
        self.mock_state.resume_active = False
        self.mock_state.current_track = None
        self.mock_state.position_seconds = 0.0

    @patch('music_player.player_shortcuts.handle_keypress')
    def test_pc1_and_pc2_shortcuts(self, mock_keypress):
        result = handle_command(self.mock_state, "")
        self.assertTrue(result)

        result = handle_command(self.mock_state, "p")
        self.assertTrue(result)
        mock_keypress.assert_called_with(self.mock_state, "p")

    @patch('music_player.player_metrics.save_data')
    def test_pc3_quit_command(self, mock_save):
        result = handle_command(self.mock_state, "/quit")
        self.assertFalse(result)
        mock_save.assert_called_once()

    @patch('music_player.player_core.play')
    @patch('music_player.player_seek.seek_to')
    def test_pc4_play_resume_with_seek(self, mock_seek, mock_play):
        self.mock_state.resume_active = True
        self.mock_state.current_track = MagicMock()
        self.mock_state.position_seconds = 45.0
        handle_command(self.mock_state, "/play")
        mock_play.assert_called_once()
        mock_seek.assert_called_with(self.mock_state, "45.0")
        self.assertFalse(self.mock_state.resume_active)

    @patch('music_player.player_core.play')
    def test_pc6_play_standard(self, mock_play):
        handle_command(self.mock_state, "/play")
        mock_play.assert_called_once()

    @patch('music_player.player_seek.seek_to')
    def test_pc13_and_pc14_seek_logic(self, mock_seek):
        with patch('builtins.print') as mock_print:
            handle_command(self.mock_state, "/seek")
            mock_print.assert_called_with("[main] Usage: /seek <mm:ss or seconds>")
            mock_seek.assert_not_called()
        handle_command(self.mock_state, "/seek 30")
        mock_seek.assert_called_with(self.mock_state, "30")

    def test_pc21_unknown_command(self):
        with patch('builtins.print') as mock_print:
            result = handle_command(self.mock_state, "/notacommand")
            self.assertTrue(result)
            mock_print.assert_called_with("Unknown command. Try /help")


if __name__ == '__main__':
    unittest.main()