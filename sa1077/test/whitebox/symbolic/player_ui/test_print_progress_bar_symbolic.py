import unittest
from unittest.mock import MagicMock, patch

from music_player.player_ui import print_progress_bar



class TestSymbolicExecution(unittest.TestCase):

    def setUp(self):

        self.mock_state = MagicMock()
        self.mock_state.__str__.return_value = "MockState"

    @patch('sys.stdout')
    @patch('music_player.player_ui.render_progress_bar')
    @patch('music_player.player_ui._ensure_player_state')
    def test_pc_1_early_return(self, mock_ensure, mock_render, mock_print):

        mock_ensure.return_value = None

        s1_input = None

        print_progress_bar(s1_input)

        mock_ensure.assert_called_once_with(s1_input, "progress_bar")
        mock_render.assert_not_called()
        mock_print.assert_not_called()

    @patch('builtins.print')
    @patch('music_player.player_ui.render_progress_bar')
    @patch('music_player.player_ui._ensure_player_state')
    def test_pc_2_render_and_print(self, mock_ensure, mock_render, mock_print):

        mock_ensure.return_value = self.mock_state
        mock_render.return_value = "████░░ 50%"

        s1_input = self.mock_state

        print_progress_bar(s1_input)

        mock_ensure.assert_called_once_with(s1_input, "progress_bar")
        mock_render.assert_called_once_with(self.mock_state)
        mock_print.assert_called_once_with("[ui] ████░░ 50%")


if __name__ == '__main__':
    unittest.main()